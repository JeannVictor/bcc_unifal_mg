package com.coinconverter.CoinConverter.controller;


import com.coinconverter.CoinConverter.dto.response.ConversionHistoricalResponse;
import com.coinconverter.CoinConverter.dto.response.TopCoinResponse;
import com.coinconverter.CoinConverter.dto.response.TopConversionResponse;
import com.coinconverter.CoinConverter.service.ConversionStatsService;
import io.swagger.v3.oas.annotations.Operation;
import lombok.RequiredArgsConstructor;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import java.time.LocalDateTime;
import java.util.List;

@RestController
@RequiredArgsConstructor
@RequestMapping("/api/conversion-stats")
public class PublicStatsController {

    private final ConversionStatsService conversionStatsService;

    @GetMapping("/top-conversions")
    @Operation(summary = "Get most frequent currency conversions",
            description = "Retrieves the most frequently used currency conversions by users within the specified time range.")
    public List<TopConversionResponse> topConversions(@RequestParam Integer limit,
                                                      @RequestParam(required = false) LocalDateTime begin,
                                                      @RequestParam(required = false) LocalDateTime end) {
        return conversionStatsService.getTopConversion(limit, begin, end);
    }

    @GetMapping("/top-from-coin")
    @Operation(summary = "Get most used source currencies",
            description = "Retrieves the currencies most frequently used as the 'from' (source) currency in conversions within the specified time range.")
    public List<TopCoinResponse> topFromCoin(@RequestParam Integer limit,
                                             @RequestParam(required = false) LocalDateTime begin,
                                             @RequestParam(required = false) LocalDateTime end) {
        return conversionStatsService.getTopFromCoin(limit, begin, end);
    }

    @GetMapping("/top-to-coins")
    @Operation(summary = "Get most used target currencies",
            description = "Retrieves the currencies most frequently used as the 'to' (target) currency in conversions within the specified time range.")
    public List<TopCoinResponse> topToCoin(@RequestParam Integer limit,
                                           @RequestParam(required = false) LocalDateTime begin,
                                           @RequestParam(required = false) LocalDateTime end) {
        return conversionStatsService.getTopToCoin(limit, begin, end);
    }

    @GetMapping("/historical-conversions")
    @Operation(summary = "Get conversion history",
            description = "Retrieves the historical record of currency conversions performed on the site.")
    public List<ConversionHistoricalResponse> historicalConversions(@RequestParam Integer limit) {
        return conversionStatsService.findConversionsHistory(limit);
    }
}