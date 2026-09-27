package com.coinconverter.CoinConverter.controller;

import com.coinconverter.CoinConverter.dto.response.DashboardResponse;
import com.coinconverter.CoinConverter.service.DashboardExportService;
import com.coinconverter.CoinConverter.service.DashboardService;
import com.coinconverter.CoinConverter.util.AuthHelper;
import io.swagger.v3.oas.annotations.Operation;
import lombok.RequiredArgsConstructor;
import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.security.core.Authentication;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import java.time.LocalDateTime;

@RestController
@RequestMapping("/api/dashboard")
@RequiredArgsConstructor
public class DashboardController {

    private final DashboardService dashboardService;
    private final DashboardExportService dashboardExportService;
    private final AuthHelper authHelper;


    @GetMapping("/dashboard")
    @Operation(summary = "Get your statistics quickly in a dashboard. ", description = "Get all of your statistics quickly in a dashboard. ")
    public DashboardResponse getDashboard(Authentication authentication, @RequestParam(required = false) Integer limit,
                                          @RequestParam(required = false) LocalDateTime start,
                                          @RequestParam(required = false) LocalDateTime end) {

        String userEmail = authHelper.getUserEmail(authentication);
        return dashboardService.getDashboard(userEmail, limit, start, end);
    }

    @GetMapping("/export")
    @Operation(summary = "Export your dashboard as JSON/CSV", description = "Get your dashboard in JSON/CSV format so you can have all your statistics locally. ")
    public ResponseEntity<String> exportAsJsonOrCsv(Authentication authentication, @RequestParam(defaultValue = "JSON") String format,
                                                    @RequestParam(required = false) Integer limit,
                                                    @RequestParam(required = false) LocalDateTime start,
                                                    @RequestParam(required = false) LocalDateTime end) {

        String userEmail = authHelper.getUserEmail(authentication);
        String export = dashboardExportService.exportDashboard(userEmail, format, limit, start, end);

        MediaType mediaType = format.equalsIgnoreCase("CSV")
                ? MediaType.valueOf("text/csv")
                : MediaType.APPLICATION_JSON;

        return ResponseEntity.ok()
                .header(HttpHeaders.CONTENT_DISPOSITION,
                        "attachment; filename=dashboard." + format.toLowerCase())
                .contentType(mediaType)
                .body(export);
    }
}

