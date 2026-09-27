package com.coinconverter.CoinConverter.controller;

import com.coinconverter.CoinConverter.dto.response.FavoriteCoinResponse;
import com.coinconverter.CoinConverter.service.FavoriteCoinService;
import com.coinconverter.CoinConverter.util.AuthHelper;
import io.swagger.v3.oas.annotations.Operation;
import lombok.RequiredArgsConstructor;
import org.springframework.security.core.Authentication;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequiredArgsConstructor
@RequestMapping("/api/favorite-coin")
public class FavoriteCoinController {

    private final FavoriteCoinService favoriteCoinService;
    private final AuthHelper authHelper;

    @PostMapping("favorite-a-coin")
    @Operation(summary = "Favorite a coin ", description = "Favoriting a currency makes your life easier in future actions.")
    public FavoriteCoinResponse favoriteACoin(Authentication authentication, @RequestParam String coin) {

        String userEmail = authHelper.getUserEmail(authentication);

        return favoriteCoinService.favoriteCoin(userEmail, coin);
    }

    @DeleteMapping("/delete-favorite-coins")
    @Operation(summary = "Delete a coin ", description = "You basically remove a coin from your list of favorite coins. ")
    public void deleteFavoriteCoin(Authentication authentication, @RequestParam String coin) {

        String userEmail = authHelper.getUserEmail(authentication);

        favoriteCoinService.deleteFavoriteCoin(userEmail, coin);
    }

    @GetMapping("/favorite-coins-user")
    @Operation(summary = "Get all of your favorite coins ", description = "You can see all your coins in one place. ")
    public List<FavoriteCoinResponse> getUserFavoriteCoins(Authentication authentication) {

        String userEmail = authHelper.getUserEmail(authentication);

        return favoriteCoinService.getUserFavoriteCoins(userEmail);
    }

}
