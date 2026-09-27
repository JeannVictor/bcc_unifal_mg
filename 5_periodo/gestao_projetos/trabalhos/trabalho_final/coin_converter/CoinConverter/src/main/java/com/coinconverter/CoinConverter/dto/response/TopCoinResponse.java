package com.coinconverter.CoinConverter.dto.response;

import lombok.*;

import java.math.BigDecimal;

@Getter
@Setter
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class TopCoinResponse {

    private String coin;
    private Long totalConversions;
    private BigDecimal totalPercentage;
}
