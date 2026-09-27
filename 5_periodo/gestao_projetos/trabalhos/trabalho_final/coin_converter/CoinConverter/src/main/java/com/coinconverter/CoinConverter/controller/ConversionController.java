package com.coinconverter.CoinConverter.controller;

import com.coinconverter.CoinConverter.dto.request.ConversionRequest;
import com.coinconverter.CoinConverter.dto.response.ConversionResponse;
import com.coinconverter.CoinConverter.service.ConversionService;
import com.coinconverter.CoinConverter.util.AuthHelper;
import io.swagger.v3.oas.annotations.Operation;
import lombok.RequiredArgsConstructor;
import org.springframework.security.core.Authentication;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/conversion")
@RequiredArgsConstructor
public class ConversionController {

    private final ConversionService conversionService;
    private final AuthHelper authHelper;

    @PostMapping
    @Operation(summary = "Get the conversion between two coins", description = "Get the result of a conversion from a coin in another coin ")
    public ConversionResponse convert(@RequestBody ConversionRequest request, Authentication authentication) {

        String userEmail = authHelper.getUserEmail(authentication);

        return conversionService.convert(
                request.getAmount(),
                request.getFromCoin(),
                request.getToCoin(),
                userEmail
        );
    }
}