package com.coinconverter.CoinConverter.security;

import com.coinconverter.CoinConverter.repository.UserRepository;
import com.coinconverter.CoinConverter.service.JwtService;
import jakarta.servlet.FilterChain;
import jakarta.servlet.ServletException;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import lombok.extern.log4j.Log4j2;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.stereotype.Component;
import org.springframework.web.filter.OncePerRequestFilter;

import java.io.IOException;

@Log4j2
@Component
public class JwtSecurityFilter extends OncePerRequestFilter {

    private final UserRepository userRepository;
    private final JwtService jwtService;

    public JwtSecurityFilter(UserRepository userRepository, JwtService jwtService) {
        this.userRepository = userRepository;
        this.jwtService = jwtService;
        log.info("=== JwtSecurityFilter CRIADO ===");
    }

    @Override
    protected void doFilterInternal(HttpServletRequest request, HttpServletResponse response, FilterChain filterChain)
            throws ServletException, IOException {

        String uri = request.getRequestURI();
        String method = request.getMethod();

        log.info("=== FILTRO JWT EXECUTADO ===");
        log.info("URI: {} {}", method, uri);

        var token = recoverToken(request);

        if (token != null) {
            log.info("Token encontrado no header");
            try {
                var subject = jwtService.validateToken(token);
                log.info("Token validado para: {}", subject);

                var userOptional = userRepository.findByEmail(subject);

                if (userOptional.isPresent()) {
                    var user = userOptional.get();
                    var authentication = new UsernamePasswordAuthenticationToken(
                            user, null, user.getAuthorities()
                    );
                    SecurityContextHolder.getContext().setAuthentication(authentication);
                    log.info("Usuário autenticado: {}", subject);
                } else {
                    log.warn("Token válido mas usuário não encontrado: {}", subject);
                }
            } catch (Exception e) {
                log.error(" Erro ao validar token: {}", e.getMessage());
            }
        } else {
            log.info("Sem token - requisição anônima");
        }

        filterChain.doFilter(request, response);
    }

    private String recoverToken(HttpServletRequest request) {
        var header = request.getHeader("Authorization");
        if (header == null) {
            log.info("Header Authorization não encontrado");
            return null;
        }

        String token = header.replace("Bearer ", "");
        log.info("Token extraído (primeiros 20 chars): {}...",
                token.length() > 20 ? token.substring(0, 20) : token);
        return token;
    }
}