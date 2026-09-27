package com.coinconverter.CoinConverter.exception;


import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.RestControllerAdvice;

import java.time.LocalDateTime;
import java.util.Map;

@RestControllerAdvice
public class GlobalExceptionHandler {
    //------------------------------------------------------------------------------------------------------------------------------------
    // ERRO 400 : O usuario passou para o sistema algo inválido
    @ExceptionHandler(CoinNotFoundException.class)
    public ResponseEntity<?> handleCoinNotFound(CoinNotFoundException ex) {
        return ResponseEntity
                .status(HttpStatus.BAD_REQUEST)
                .body(error(ex.getMessage(), HttpStatus.BAD_REQUEST));
    }

    @ExceptionHandler(EqualCoinsException.class)
    public ResponseEntity<?> handleEqualCoins(EqualCoinsException ex) {
        return ResponseEntity
                .status(HttpStatus.BAD_REQUEST)
                .body(error(ex.getMessage(), HttpStatus.BAD_REQUEST));
    }

    @ExceptionHandler(NegativeAmountException.class)
    public ResponseEntity<?> handleNegativeAmount(NegativeAmountException ex) {
        return ResponseEntity
                .status(HttpStatus.BAD_REQUEST)
                .body(error(ex.getMessage(), HttpStatus.BAD_REQUEST));
    }
    //------------------------------------------------------------------------------------------------------------------------------------
    // ERRO 401 : Servidor recebeu a requisição, mas não a processou porque o cliente não está autenticado ou possui credenciais inválidas

    @ExceptionHandler(InvalidCredentialsException.class)
    public ResponseEntity<?> handleInvalidCredentials(InvalidCredentialsException ex) {
        return ResponseEntity
                .status(HttpStatus.UNAUTHORIZED)
                .body(error(ex.getMessage(), HttpStatus.UNAUTHORIZED));
    }

    @ExceptionHandler(UserNotAuthenticationException.class)
    public ResponseEntity<?> handleUserNotAuthentication(UserNotAuthenticationException ex) {
        return ResponseEntity
                .status(HttpStatus.UNAUTHORIZED)
                .body(error(ex.getMessage(), HttpStatus.UNAUTHORIZED));
    }

    //------------------------------------------------------------------------------------------------------------------------------------
    // ERRO 404: Not found
    @ExceptionHandler(ConversionNotFoundException.class)
    public ResponseEntity<?> handleConversionNotFound(ConversionNotFoundException ex) {
        return ResponseEntity
                .status(HttpStatus.NOT_FOUND)
                .body(error(ex.getMessage(), HttpStatus.NOT_FOUND));
    }

    //------------------------------------------------------------------------------------------------------------------------------------
    // ERRO 409: Solitação do usuario entra em conflito
    @ExceptionHandler(DuplicateEmailException.class)
    public ResponseEntity<?> handleDuplicateEmail(DuplicateEmailException ex) {
        return ResponseEntity
                .status(HttpStatus.CONFLICT)
                .body(error(ex.getMessage(), HttpStatus.CONFLICT));
    }

    @ExceptionHandler(FavoriteCoinAlreadyExistsException.class)
    public ResponseEntity<?> handleFavoriteCoinAlreadyExists(FavoriteCoinAlreadyExistsException ex) {
        return ResponseEntity
                .status(HttpStatus.CONFLICT)
                .body(error(ex.getMessage(), HttpStatus.CONFLICT));
    }

    //------------------------------------------------------------------------------------------------------------------------------------
    // ERRO 502: Falha de comunicação dos servidores na internet
    @ExceptionHandler(RequisitionErrorException.class)
    public ResponseEntity<?> handleRequisitionError(RequisitionErrorException ex) {
        return ResponseEntity
                .status(HttpStatus.BAD_GATEWAY)
                .body(error(ex.getMessage(), HttpStatus.BAD_GATEWAY));
    }

    //------------------------------------------------------------------------------------------------------------------------------------
    // ERRO 503: Servidor web temporariamente indisponível, sobrecarregado ou em manutenção, impedindo o processamento da solicitação

    @ExceptionHandler(RateUnavailableException.class)
    public ResponseEntity<?> handleRateUnavailable(RateUnavailableException ex) {
        return ResponseEntity
                .status(HttpStatus.SERVICE_UNAVAILABLE)
                .body(error(ex.getMessage(), HttpStatus.SERVICE_UNAVAILABLE));
    }


    private Map<String, Object> error(String message, HttpStatus status) {
        return Map.of(
                "timestamp", LocalDateTime.now(),
                "status", status.value(),
                "error", message
        );
    }
}
