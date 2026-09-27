package com.coinconverter.CoinConverter.provider.dto;

import lombok.AllArgsConstructor;
import lombok.Data;

import java.math.BigDecimal;
import java.time.LocalDateTime;

@Data
@AllArgsConstructor
public class RateCacheEntry {
    private BigDecimal rate;
    private LocalDateTime lastUpdated;
}
