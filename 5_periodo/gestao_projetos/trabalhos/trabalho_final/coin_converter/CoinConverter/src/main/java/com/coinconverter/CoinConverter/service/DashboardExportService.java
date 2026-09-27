package com.coinconverter.CoinConverter.service;

import com.coinconverter.CoinConverter.dto.response.*;
import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import lombok.RequiredArgsConstructor;
import lombok.extern.log4j.Log4j2;
import org.springframework.stereotype.Service;

import java.time.LocalDateTime;
import java.util.List;

@Log4j2
@Service
@RequiredArgsConstructor
public class DashboardExportService {

    private final DashboardService dashboardService;

    public String exportDashboard(String userEmail, String format, Integer limit, LocalDateTime start, LocalDateTime end) {

        // Retrieve the data to be exported as CSV or JSON
        DashboardResponse dashboardResponse = dashboardService.getDashboard(userEmail, limit, start, end);

        // Convert the response to CSV or JSON format
        if (format == null || format.equals("JSON")) {
            return toJson(dashboardResponse);
        } else if (format.equals("CSV")) {
            return toCsv(dashboardResponse);
        } else {
            throw new RuntimeException("Invalid format");
        }
    }

    private String toJson(DashboardResponse dashboard) {
        try {
            ObjectMapper objectMapper = new ObjectMapper();
            return objectMapper.writeValueAsString(dashboard);
        } catch (JsonProcessingException e) {
            throw new RuntimeException("Error generating JSON", e);
        }
    }

    private String toCsv(DashboardResponse dashboard) {
        StringBuilder csv = new StringBuilder();

        // 1. Conversion history
        csv.append("\n=== CONVERSION HISTORY ===\n");
        csv.append("Source Currency,Target Currency,Amount,Rate,Converted Amount,Date\n");

        List<ConversionHistoricalResponse> history = dashboard.getUserHistory();
        for (int i = 0; i < history.size(); i++) {
            ConversionHistoricalResponse c = history.get(i);
            csv.append(c.getFromCoin()).append(",")
                    .append(c.getToCoin()).append(",")
                    .append(c.getAmount()).append(",")
                    .append(c.getRate()).append(",")
                    .append(c.getConvertedAmount()).append(",")
                    .append("\n");
        }

        // 2. Favorite currencies
        csv.append("\n=== FAVORITE CURRENCIES ===\n");
        csv.append("Currency Name\n");

        List<FavoriteCoinResponse> favoriteCoins = dashboard.getFavoriteCoins();
        for (int i = 0; i < favoriteCoins.size(); i++) {
            FavoriteCoinResponse f = favoriteCoins.get(i);
            csv.append(f.getCoinName()).append("\n");
        }

        // 3. Most frequent conversions (TopConversionResponse)
        csv.append("\n=== MOST FREQUENT CONVERSIONS ===\n");
        csv.append("Source Currency,Target Currency,Total Conversions,Total Percentage\n");

        List<TopConversionResponse> topConversions = dashboard.getTopConversionsLast30Days();
        for (int i = 0; i < topConversions.size(); i++) {
            TopConversionResponse tc = topConversions.get(i);
            csv.append(tc.getFromCoin()).append(",")
                    .append(tc.getToCoin()).append(",")
                    .append(tc.getTotalConversions()).append(",")
                    .append(tc.getTotalPercentage()).append("\n");
        }

        // 4. Most used source currencies
        csv.append("\n=== MOST USED SOURCE CURRENCIES ===\n");
        csv.append("Currency,Total Conversions,Total Percentage\n");

        List<TopCoinResponse> topFromCoin = dashboard.getTopFromCoinsLast30Days();
        for (int i = 0; i < topFromCoin.size(); i++) {
            TopCoinResponse tfc = topFromCoin.get(i);
            csv.append(tfc.getCoin()).append(",")
                    .append(tfc.getTotalConversions()).append(",")
                    .append(tfc.getTotalPercentage()).append("\n");
        }

        // 5. Most used target currencies
        csv.append("\n=== MOST USED TARGET CURRENCIES ===\n");
        csv.append("Currency,Total Conversions,Total Percentage\n");

        List<TopCoinResponse> topToCoin = dashboard.getTopToCoinsLast30Days();
        for (int i = 0; i < topToCoin.size(); i++) {
            TopCoinResponse tfc = topToCoin.get(i);
            csv.append(tfc.getCoin()).append(",")
                    .append(tfc.getTotalConversions()).append(",")
                    .append(tfc.getTotalPercentage()).append("\n");
        }

        return csv.toString();
    }
}