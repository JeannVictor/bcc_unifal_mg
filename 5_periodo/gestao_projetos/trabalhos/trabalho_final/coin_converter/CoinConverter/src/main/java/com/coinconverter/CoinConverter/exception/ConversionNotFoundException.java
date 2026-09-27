package com.coinconverter.CoinConverter.exception;

public class ConversionNotFoundException extends RuntimeException {
    public ConversionNotFoundException(String message) {
        super(message);
    }
}
