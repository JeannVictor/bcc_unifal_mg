package com.coinconverter.CoinConverter.service;

import com.coinconverter.CoinConverter.dto.response.ConversionResponse;
import com.coinconverter.CoinConverter.entity.Conversion;
import com.coinconverter.CoinConverter.exception.CoinNotFoundException;
import com.coinconverter.CoinConverter.exception.EqualCoinsException;
import com.coinconverter.CoinConverter.exception.NegativeAmountException;
import com.coinconverter.CoinConverter.repository.ConversionRepository;
import jakarta.transaction.Transactional;
import lombok.RequiredArgsConstructor;
import lombok.extern.log4j.Log4j2;
import org.springframework.stereotype.Service;

import java.math.BigDecimal;


@Log4j2
@Service
@RequiredArgsConstructor
public class ConversionService {

    private final RateCacheService rateCacheService;
    private final ConversionRepository conversionRepository;

    @Transactional
    public ConversionResponse convert(BigDecimal amount, String from, String to, String userEmail) {
        log.debug("Converting {} from {} to {}", amount, from, to);
        int result = amount.compareTo(BigDecimal.ZERO);
        // If the amount to be converted is negative or zero, conversion is not possible
        if (result <= 0) {
            throw new NegativeAmountException("Unable to convert a negative or null amount");
        }

        // Validate if the currency codes are valid
        if (!isValidCurrencyCode(from) || !isValidCurrencyCode(to)) {
            throw new CoinNotFoundException("Unable to convert a non-existing coin");
        }

        // Convert currency codes to uppercase
        from = from.toUpperCase();
        to = to.toUpperCase();

        if (from.equals(to)) {
            throw new EqualCoinsException("Unable to convert " + from + " to " + to);
        }

        // Get the conversion rate between the currencies
        BigDecimal rate = rateCacheService.getRate(from, to);

        // Perform the currency conversion
        BigDecimal amountConverted = amount.multiply(rate);

        // Save the conversion to the database
        Conversion conversion = Conversion.builder()
                .amount(amount)
                .fromCoin(from)
                .toCoin(to)
                .rate(rate)
                .convertedAmount(amountConverted)
                .userEmail(userEmail)
                .build();

        conversionRepository.save(conversion);

        // Return the conversion result
        return new ConversionResponse(
                amount,
                from,
                to,
                rate,
                amountConverted
        );
    }

    // Function to validate currency code acronym
    private Boolean isValidCurrencyCode(String acronym) {
        return acronym != null && acronym.matches("[A-Za-z]{3}");
    }
}