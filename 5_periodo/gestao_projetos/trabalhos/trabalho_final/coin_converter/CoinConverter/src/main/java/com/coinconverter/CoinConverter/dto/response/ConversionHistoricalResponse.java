package com.coinconverter.CoinConverter.dto.response;

import lombok.*;

import java.math.BigDecimal;
import java.time.LocalDateTime;

@Getter
@Setter
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class ConversionHistoricalResponse {

    private String fromCoin;

    private String toCoin;

    private BigDecimal amount;

    private BigDecimal rate;

    private BigDecimal convertedAmount;

    private LocalDateTime convertedDateTime;
}
