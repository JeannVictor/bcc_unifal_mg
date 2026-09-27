package com.coinconverter.CoinConverter.dto.response;

import lombok.*;

import java.math.BigDecimal;

@Getter
@Setter
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class ConversionResponse {
    private BigDecimal originalAmount;
    private String fromCoin;
    private String toCoin;
    private BigDecimal rate;
    private BigDecimal convertedAmount;

}
