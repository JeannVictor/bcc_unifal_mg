package com.coinconverter.CoinConverter.exception;

public class FavoriteCoinAlreadyExistsException extends RuntimeException {
    public FavoriteCoinAlreadyExistsException(String message) {
        super(message);
    }
}
