package com.coinconverter.CoinConverter.repository;

import com.coinconverter.CoinConverter.entity.User;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.Optional;

@Repository
public interface UserRepository extends JpaRepository<User, Long> {

    // Query that returns a user by their email
    Optional<User> findByEmail(String email);

    // Check if a user exists with the given email
    boolean existsByEmail(String email);
}