package com.musicstore.bluevelvet.domain.service;

import com.musicstore.bluevelvet.api.request.LoginRequest;
import com.musicstore.bluevelvet.api.request.RegisterRequest;
import com.musicstore.bluevelvet.api.response.AuthResponse;
import com.musicstore.bluevelvet.domain.exception.DuplicateEmailException;
import com.musicstore.bluevelvet.domain.exception.InvalidCredentialsException;
import com.musicstore.bluevelvet.infrastructure.entity.User;
import com.musicstore.bluevelvet.infrastructure.repository.UserRepository;
import lombok.RequiredArgsConstructor;
import lombok.extern.log4j.Log4j2;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.stereotype.Service;

@Log4j2
@Service
@RequiredArgsConstructor
public class AuthService {

    private final UserRepository userRepository;
    private final BCryptPasswordEncoder passwordEncoder = new BCryptPasswordEncoder();

    /**
     * US-1603: Register new user
     */
    public AuthResponse register(RegisterRequest request) {
        log.debug("Trying to register user with email {}", request.getEmail());

        if (userRepository.findByEmail(request.getEmail()).isPresent()) {
            log.error("User with email {} already exists", request.getEmail());
            throw new DuplicateEmailException("User with email " + request.getEmail() + " already exists");
        }

        if (request.getPassword().length() < 8) {
            throw new IllegalArgumentException("Password must be at least 8 characters long");
        }

        if (!request.getPassword().equals(request.getConfirmPassword())) {
            throw new IllegalArgumentException("Passwords do not match");
        }

        User newUser = User.builder()
                .email(request.getEmail())
                .password(passwordEncoder.encode(request.getPassword()))
                .userRole(request.getRole())
                .enabled(true)
                .build();

        User saved = userRepository.save(newUser);
        log.info("User registered successfully: {}", saved.getEmail());

        return AuthResponse.builder()
                .id(saved.getId())
                .email(saved.getEmail())
                .role(saved.getUserRole())
                .message("User registered successfully")
                .build();
    }

    /**
     * US-1232: User login
     */
    public AuthResponse login(LoginRequest request) {
        log.debug("Trying to login user with email {}", request.getEmail());

        User user = userRepository.findByEmail(request.getEmail())
                .orElseThrow(() -> {
                    log.error("User not found: {}", request.getEmail());
                    return new InvalidCredentialsException("Incorrect email or password. Please try again");
                });

        if (!passwordEncoder.matches(request.getPassword(), user.getPassword())) {
            log.error("Invalid password for user: {}", request.getEmail());
            throw new InvalidCredentialsException("Incorrect email or password. Please try again");
        }

        log.info("Login successful: {}", user.getEmail());

        return AuthResponse.builder()
                .id(user.getId())
                .email(user.getEmail())
                .role(user.getUserRole())
                .message("Login successful. Welcome, " + user.getEmail() + " (" + user.getUserRole() + ")")
                .build();
    }
}
