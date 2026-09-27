package com.coinconverter.CoinConverter.dto.response;

import lombok.*;

import java.math.BigDecimal;

@Getter
@Setter
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class TopConversionResponse {

    private String fromCoin;
    private String toCoin;
    private Long totalConversions;
    private BigDecimal totalPercentage;
}
