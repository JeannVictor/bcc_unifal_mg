package com.coinconverter.CoinConverter.provider;

import com.coinconverter.CoinConverter.exception.ConversionNotFoundException;
import com.coinconverter.CoinConverter.exception.RateUnavailableException;
import com.coinconverter.CoinConverter.exception.RequisitionErrorException;
import com.coinconverter.CoinConverter.provider.dto.RateProviderResponse;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;
import org.springframework.web.client.ResourceAccessException;
import org.springframework.web.client.RestTemplate;

import java.math.BigDecimal;

@Component
public class RateProvider {

    @Value("${api.exchange.key}")
    String apiKey;

    public BigDecimal getRate(String from, String to) {

        // Format the API URL to match the correct structure
        String url = String.format("https://v6.exchangerate-api.com/v6/%s/latest/%s", apiKey, from);

        // Perform a GET request to the API
        RestTemplate restTemplate = new RestTemplate();
        RateProviderResponse response;

        // Handle potential API errors
        try {
            response = restTemplate.getForObject(url, RateProviderResponse.class);
        } catch (ResourceAccessException e) {
            throw new RateUnavailableException("The service could not be accessed. Cause: " + e.getMessage());
        } catch (Exception e) {
            throw new RequisitionErrorException("Request error. Cause: " + e.getMessage());
        }

        // Check for invalid response from the API
        if (response == null || response.getConversionRates() == null) {
            throw new RequisitionErrorException("Invalid response from rate provider");
        }

        BigDecimal rate = response.getConversionRates().get(to);

        // Return the rate value or throw an error
        if (rate == null) {
            throw new ConversionNotFoundException("Conversion rate not found");
        }
        return rate;
    }
}