package com.musicstore.bluevelvet.api.controller;

import com.musicstore.bluevelvet.api.request.LoginRequest;
import com.musicstore.bluevelvet.api.request.RegisterRequest;
import com.musicstore.bluevelvet.api.response.AuthResponse;
import com.musicstore.bluevelvet.domain.service.AuthService;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import lombok.extern.log4j.Log4j2;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@Log4j2
@RestController
@RequestMapping("/api/auth")
@RequiredArgsConstructor
@CrossOrigin(origins = "*")
@Tag(name = "Authentication", description = "User authentication APIs")
public class AuthController {

    private final AuthService authService;

    @GetMapping("/")
    public String redirectToLogin() {
        return "redirect:/login";
    }


    /**
     * US-1603: Register new user
     */
    @PostMapping("/register")
    @Operation(summary = "Register new user", description = "Register a new user in the system (US-1603)")
    public ResponseEntity<AuthResponse> register(@Valid @RequestBody RegisterRequest request) {
        log.info("POST /api/auth/register - Email: {}", request.getEmail());
        AuthResponse response = authService.register(request);
        return ResponseEntity.status(HttpStatus.CREATED).body(response);
    }

    /**
     * US-1232: Login
     */
    @PostMapping("/login")
    @Operation(summary = "User login", description = "Authenticate user with email and password (US-1232)")
    public ResponseEntity<AuthResponse> login(@Valid @RequestBody LoginRequest request) {
        log.info("POST /api/auth/login - Email: {}", request.getEmail());
        AuthResponse response = authService.login(request);
        return ResponseEntity.ok(response);
    }
}