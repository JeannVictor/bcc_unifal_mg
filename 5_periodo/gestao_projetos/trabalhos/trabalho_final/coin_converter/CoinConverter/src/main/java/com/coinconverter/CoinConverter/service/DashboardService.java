package com.coinconverter.CoinConverter.service;

import com.coinconverter.CoinConverter.dto.response.*;
import lombok.RequiredArgsConstructor;
import lombok.extern.log4j.Log4j2;
import org.springframework.stereotype.Service;

import java.time.LocalDateTime;
import java.util.List;

@Log4j2
@Service
@RequiredArgsConstructor
public class DashboardService {

    private final ConversionStatsLoggedService conversionStatsLoggedService;
    private final FavoriteCoinService favoriteCoinService;

    public DashboardResponse getDashboard(String userEmail, Integer limit, LocalDateTime startDateTime, LocalDateTime endDateTime) {
        // Set default values if both parameters are null
        LocalDateTime end = LocalDateTime.now();
        LocalDateTime start = end.minusDays(30);

        if (limit == null || limit < 1) {
            limit = 5;
        }

        // Handle different parameter combinations
        if (startDateTime == null && endDateTime != null) {
            start = LocalDateTime.of(2026, 1, 1, 0, 0);
            end = endDateTime;
        } else if (startDateTime != null && endDateTime == null) {
            start = startDateTime;
        }

        // Get user's conversion history
        List<ConversionHistoricalResponse> userConversions = conversionStatsLoggedService.findUserHistory(userEmail);

        // Get user's favorite currencies
        List<FavoriteCoinResponse> userFavoriteCoins = favoriteCoinService.getUserFavoriteCoins(userEmail);

        // Get user's top N conversions from the last 30 days (or specified period)
        List<TopConversionResponse> userTopConversions = conversionStatsLoggedService.getTopConversionByUser(userEmail, limit, start, end);

        // Get user's top N most used target currencies from the last 30 days (or specified period)
        List<TopCoinResponse> userTopToCoins = conversionStatsLoggedService.getTopToCoinByUser(userEmail, limit, start, end);

        // Get user's top N most used source currencies from the last 30 days (or specified period)
        List<TopCoinResponse> userTopFromCoins = conversionStatsLoggedService.getTopFromCoinByUser(userEmail, limit, start, end);

        return DashboardResponse.builder()
                .userHistory(userConversions)
                .favoriteCoins(userFavoriteCoins)
                .topFromCoinsLast30Days(userTopFromCoins)
                .topToCoinsLast30Days(userTopToCoins)
                .topConversionsLast30Days(userTopConversions)
                .build();
    }
}