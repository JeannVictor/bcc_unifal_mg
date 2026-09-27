package com.coinconverter.CoinConverter.service;

import com.coinconverter.CoinConverter.exception.RateUnavailableException;
import com.coinconverter.CoinConverter.provider.RateProvider;
import com.coinconverter.CoinConverter.provider.dto.RateCacheEntry;
import lombok.RequiredArgsConstructor;
import lombok.extern.log4j.Log4j2;
import org.springframework.stereotype.Service;

import java.math.BigDecimal;
import java.time.Duration;
import java.time.LocalDateTime;
import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;

@Log4j2
@Service
@RequiredArgsConstructor
public class RateCacheService {

    private final RateProvider rateProvider;
    private final int expirationTime = 20;

    private final Map<String, RateCacheEntry> cache = new ConcurrentHashMap<>();

    public BigDecimal getRate(String from, String to) {
        String key = getKey(from, to);
        // Check if there is a valid cache entry for this key

        // If valid, simply return the cached value
        if (isCacheValid(key)) {
            log.info("Returning cached value for key: {} (cache is valid)", key);
            return cache.get(key).getRate();
        }

        try {
            BigDecimal newRate = rateProvider.getRate(from, to);
            cache.put(key, new RateCacheEntry(newRate, LocalDateTime.now()));
            return newRate;
        } catch (Exception e) {
            if (cache.containsKey(key)) {
                log.info("Returning stale cached value for key: {} (API unavailable)", key);
                return cache.get(key).getRate();
            }
            // The API is down and this key is not in the cache
            throw new RateUnavailableException("Rate service unavailable");
        }
    }

    // Generate the key for hash map access
    private String getKey(String from, String to) {
        return from + "->" + to;
    }

    // Check if this key exists in the hash map, and if it exists, whether it's still valid
    private boolean isCacheValid(String key) {
        if (!cache.containsKey(key)) {
            return false;
        }

        LocalDateTime lastUpdated = cache.get(key).getLastUpdated();
        return (Duration.between(lastUpdated, LocalDateTime.now()).toMinutes() < expirationTime);
    }
}