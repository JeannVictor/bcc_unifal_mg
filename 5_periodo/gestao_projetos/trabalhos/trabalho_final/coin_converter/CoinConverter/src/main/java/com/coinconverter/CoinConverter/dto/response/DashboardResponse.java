package com.coinconverter.CoinConverter.dto.response;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.util.List;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class DashboardResponse {
    private List<ConversionHistoricalResponse> userHistory;
    private List<FavoriteCoinResponse> favoriteCoins;
    private List<TopConversionResponse> topConversionsLast30Days;
    private List<TopCoinResponse> topFromCoinsLast30Days;
    private List<TopCoinResponse> topToCoinsLast30Days;
}