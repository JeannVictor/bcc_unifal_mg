package com.coinconverter.CoinConverter.dto.request;

import jakarta.validation.constraints.DecimalMin;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Size;
import lombok.*;

import java.math.BigDecimal;

@Getter
@Setter
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class ConversionRequest {

    @NotNull(message = "Amount is required")
    @DecimalMin(value = "0.01", message = "Amount must be greater than 0")
    private BigDecimal amount;


    @NotBlank(message = "From coin is required")
    @Size(min = 3, max = 3, message = "Coin code must be exactly 3 characters")
    private String fromCoin;

    @NotBlank(message = "To coin is required")
    @Size(min = 3, max = 3, message = "Coin code must be exactly 3 characters")
    private String toCoin;
}
