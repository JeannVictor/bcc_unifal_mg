package com.coinconverter.CoinConverter.controller;


import com.coinconverter.CoinConverter.dto.response.ConversionHistoricalResponse;
import com.coinconverter.CoinConverter.dto.response.TopCoinResponse;
import com.coinconverter.CoinConverter.dto.response.TopConversionResponse;
import com.coinconverter.CoinConverter.service.ConversionStatsLoggedService;
import com.coinconverter.CoinConverter.util.AuthHelper;
import io.swagger.v3.oas.annotations.Operation;
import lombok.RequiredArgsConstructor;
import org.springframework.security.core.Authentication;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import java.time.LocalDateTime;
import java.util.List;

@RestController
@RequiredArgsConstructor
@RequestMapping("/api/conversion-stats-by-user")
public class UserStatsController {

    private final ConversionStatsLoggedService conversionStatsLoggedService;
    private final AuthHelper authHelper;

    @GetMapping("/top-conversions-by-user")
    @Operation(
            summary = "Get user's most frequent conversions",
            description = "Retrieves the most frequently performed currency conversions by the authenticated user within the specified time range."
    )
    public List<TopConversionResponse> topConversionsByUser(Authentication authentication, @RequestParam int limit,
                                                            @RequestParam(required = false) LocalDateTime begin,
                                                            @RequestParam(required = false) LocalDateTime end) {

        String userEmail = authHelper.isAuthenticated(authentication);
        return conversionStatsLoggedService.getTopConversionByUser(userEmail, limit, begin, end);
    }

    @GetMapping("/top-from-coin-by-user")
    @Operation(
            summary = "Get user's most used source currencies",
            description = "Retrieves the currencies most frequently used as the 'from' (source) currency by the authenticated user within the specified time range."
    )
    public List<TopCoinResponse> topFromCoinByUser(Authentication authentication, @RequestParam int limit,
                                                   @RequestParam(required = false) LocalDateTime begin,
                                                   @RequestParam(required = false) LocalDateTime end) {

        String userEmail = authHelper.isAuthenticated(authentication);
        return conversionStatsLoggedService.getTopFromCoinByUser(userEmail, limit, begin, end);
    }

    @GetMapping("/top-to-coins-by-user")
    @Operation(
            summary = "Get user's most used target currencies",
            description = "Retrieves the currencies most frequently used as the 'to' (target) currency by the authenticated user within the specified time range."
    )
    public List<TopCoinResponse> topToCoinByUser(Authentication authentication, @RequestParam int limit,
                                                 @RequestParam(required = false) LocalDateTime begin,
                                                 @RequestParam(required = false) LocalDateTime end) {

        String userEmail = authHelper.isAuthenticated(authentication);
        return conversionStatsLoggedService.getTopToCoinByUser(userEmail, limit, begin, end);
    }

    @GetMapping("/historical-conversions-by-user")
    @Operation(
            summary = "Get user's conversion history",
            description = "Retrieves the complete historical record of currency conversions performed by the authenticated user."
    )
    public List<ConversionHistoricalResponse> historicalConversionsByUser(Authentication authentication) {

        String userEmail = authHelper.isAuthenticated(authentication);
        return conversionStatsLoggedService.findUserHistory(userEmail);
    }

}