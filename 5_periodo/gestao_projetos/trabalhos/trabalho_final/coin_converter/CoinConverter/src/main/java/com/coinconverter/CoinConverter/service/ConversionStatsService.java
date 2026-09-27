package com.coinconverter.CoinConverter.service;

import com.coinconverter.CoinConverter.dto.response.ConversionHistoricalResponse;
import com.coinconverter.CoinConverter.dto.response.TopCoinResponse;
import com.coinconverter.CoinConverter.dto.response.TopConversionResponse;
import com.coinconverter.CoinConverter.entity.Conversion;
import com.coinconverter.CoinConverter.repository.ConversionRepository;
import lombok.RequiredArgsConstructor;
import lombok.extern.log4j.Log4j2;
import org.springframework.stereotype.Service;

import java.math.BigDecimal;
import java.time.LocalDateTime;
import java.util.List;
import java.util.Map;


@Log4j2
@Service
@RequiredArgsConstructor
public class ConversionStatsService {

    private final ConversionRepository conversionRepository;

    // Return the N most frequent conversions overall
    public List<TopConversionResponse> getTopConversion(int limit, LocalDateTime begin, LocalDateTime end) {

        List<Map<String, Object>> result = conversionRepository.findTopConversions(limit, begin, end);

        return result.stream()
                .map(results -> new TopConversionResponse(
                        (String) results.get("from_coin"),
                        (String) results.get("to_coin"),
                        ((Number) results.get("total_conversions")).longValue(),
                        new BigDecimal(results.get("total_percentage").toString())
                ))
                .toList();
    }

    // Return the N most frequently used source currencies overall
    public List<TopCoinResponse> getTopFromCoin(int limit, LocalDateTime begin, LocalDateTime end) {

        List<Map<String, Object>> result =
                conversionRepository.findTopFromCoinsConversions(limit, begin, end);

        return result.stream()
                .map(results -> new TopCoinResponse(
                        (String) results.get("from_coin"),
                        ((Number) results.get("total_conversions")).longValue(),
                        new BigDecimal(results.get("total_percentage").toString())
                ))
                .toList();
    }

    // Return the N most frequently used target currencies overall
    public List<TopCoinResponse> getTopToCoin(int limit, LocalDateTime begin, LocalDateTime end) {

        List<Map<String, Object>> result =
                conversionRepository.findTopToCoinsConversions(limit, begin, end);

        return result.stream()
                .map(results -> new TopCoinResponse(
                        (String) results.get("to_coin"),
                        ((Number) results.get("total_conversions")).longValue(),
                        new BigDecimal(results.get("total_percentage").toString())
                ))
                .toList();
    }

    // Return the global conversion history (including both logged-in and anonymous users)
    public List<ConversionHistoricalResponse> findConversionsHistory(int limit) {

        List<Conversion> conversions = conversionRepository.findLastConversions(limit);

        return conversions.stream()
                .map(conversion -> new ConversionHistoricalResponse(
                        conversion.getFromCoin(),
                        conversion.getToCoin(),
                        conversion.getAmount(),
                        conversion.getRate(),
                        conversion.getConvertedAmount(),
                        conversion.getConvertedDateTime()
                ))
                .toList();
    }
}