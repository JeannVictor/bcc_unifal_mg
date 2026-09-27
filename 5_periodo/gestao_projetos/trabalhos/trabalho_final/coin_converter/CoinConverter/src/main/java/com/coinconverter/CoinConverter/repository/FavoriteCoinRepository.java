package com.coinconverter.CoinConverter.repository;

import com.coinconverter.CoinConverter.entity.FavoriteCoin;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Modifying;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.Optional;

@Repository
public interface FavoriteCoinRepository extends JpaRepository<FavoriteCoin, Long> {

    // Check if the currency is already favorited by the user
    boolean existsByUserEmailAndCoinName(String userEmail, String coinName);

    // Find a specific favorite currency
    Optional<FavoriteCoin> findByUserEmailAndCoinName(String userEmail, String coinName);

    // User removes a currency from their favorites
    @Modifying
    @Query(value = "DELETE " +
            "FROM favorite_coin " +
            "WHERE (user_email = :userEmail) " +
            "AND (coin_name = :coinName)",
            nativeQuery = true)
    void deleteFavoriteCoin(@Param("userEmail") String userEmail, @Param("coinName") String coinName);

    // User views all their favorited currencies
    @Query(value = "SELECT *" +
            "FROM favorite_coin " +
            "WHERE (user_email = :userEmail) " +
            "ORDER BY created_at DESC ",
            nativeQuery = true)
    List<FavoriteCoin> findAllFavoriteCoinsByUser(@Param("userEmail") String userEmail);
}