package com.coinconverter.CoinConverter.service;

import com.coinconverter.CoinConverter.dto.response.FavoriteCoinResponse;
import com.coinconverter.CoinConverter.entity.FavoriteCoin;
import com.coinconverter.CoinConverter.exception.FavoriteCoinAlreadyExistsException;
import com.coinconverter.CoinConverter.repository.FavoriteCoinRepository;
import jakarta.transaction.Transactional;
import lombok.RequiredArgsConstructor;
import lombok.extern.log4j.Log4j2;
import org.springframework.stereotype.Service;

import java.util.List;

@Log4j2
@Service
@RequiredArgsConstructor
public class FavoriteCoinService {

    private final FavoriteCoinRepository favoriteCoinRepository;

    public FavoriteCoinResponse favoriteCoin(String userEmail, String coinName) {
        if (favoriteCoinRepository.existsByUserEmailAndCoinName(userEmail, coinName)) {
            throw new FavoriteCoinAlreadyExistsException("This coin with name " + coinName + " is already favorite");
        }

        // Save new favorite currency to the database
        FavoriteCoin favoriteCoin = FavoriteCoin.builder()
                .coinName(coinName)
                .userEmail(userEmail)
                .build();
        favoriteCoin.setUserEmail(userEmail);
        favoriteCoinRepository.save(favoriteCoin);

        return FavoriteCoinResponse.builder()
                .coinName(coinName)
                .build();
    }

    @Transactional
    public void deleteFavoriteCoin(String userEmail, String coinName) {
        if (!favoriteCoinRepository.existsByUserEmailAndCoinName(userEmail, coinName)) {
            throw new RuntimeException("This coin with name " + coinName + " is not favorite");
        }

        // Delete from the database
        favoriteCoinRepository.deleteFavoriteCoin(userEmail, coinName);
    }

    public List<FavoriteCoinResponse> getUserFavoriteCoins(String userEmail) {

        // Search in the database
        List<FavoriteCoin> result = favoriteCoinRepository.findAllFavoriteCoinsByUser(userEmail);

        return result.stream()
                .map(results -> new FavoriteCoinResponse(results.getCoinName()))
                .toList();
    }
}