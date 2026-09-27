package com.coinconverter.CoinConverter.exception;

public class RateUnavailableException extends RuntimeException {
    public RateUnavailableException(String message) {
        super(message);
    }
}
