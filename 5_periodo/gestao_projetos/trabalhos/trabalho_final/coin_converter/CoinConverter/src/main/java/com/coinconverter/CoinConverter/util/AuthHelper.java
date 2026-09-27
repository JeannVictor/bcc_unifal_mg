package com.coinconverter.CoinConverter.util;

import com.coinconverter.CoinConverter.entity.User;
import com.coinconverter.CoinConverter.exception.UserNotAuthenticationException;
import org.springframework.security.core.Authentication;
import org.springframework.stereotype.Component;

@Component
public class AuthHelper {

    public String getUserEmail(Authentication authentication) {

        if (authentication == null || !authentication.isAuthenticated()) {
            return null;
        }

        Object principal = authentication.getPrincipal();

        if (!(principal instanceof User)) {
            return null;
        }

        User user = (User) principal;
        return user.getEmail();
    }

    public String isAuthenticated(Authentication authentication) {

        if (authentication == null || !authentication.isAuthenticated()) {
            throw new UserNotAuthenticationException("User not authenticated");
        }

        Object principal = authentication.getPrincipal();

        if (!(principal instanceof User)) {
            throw new UserNotAuthenticationException("User not authenticated");
        }

        User user = (User) principal;
        return user.getEmail();
    }
}
