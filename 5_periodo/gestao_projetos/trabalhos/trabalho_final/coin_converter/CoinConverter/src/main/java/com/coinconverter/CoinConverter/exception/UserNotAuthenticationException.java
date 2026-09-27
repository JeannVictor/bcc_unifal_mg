package com.coinconverter.CoinConverter.exception;

public class UserNotAuthenticationException extends RuntimeException {
    public UserNotAuthenticationException(String message) {
        super(message);
    }
}
