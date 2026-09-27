package com.coinconverter.CoinConverter.entity;

import jakarta.persistence.*;
import jakarta.validation.constraints.Email;
import lombok.*;
import org.hibernate.annotations.CreationTimestamp;

import java.time.LocalDateTime;

@Entity
@Getter
@Setter
@Builder
@NoArgsConstructor
@AllArgsConstructor

// Defino o nome da tabela, e o que deve ser unico dentro dela(<email,moeda>)
// De primeira instancia por erro coloquei apenas o email como unico
// (fazendo com que um usuario so favoritasse uma moeda ).
@Table(
        name = "favorite_coin",
        uniqueConstraints = {
                @UniqueConstraint(columnNames = {"user_email", "coin_name"})
        }
)
public class FavoriteCoin {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Email
    @Column(name = "user_email", nullable = false)
    private String userEmail;

    @Column(name = "coin_name", nullable = false, length = 3)
    private String coinName;

    @CreationTimestamp
    @Column(name = "created_at", nullable = false, updatable = false)
    private LocalDateTime createdAt;
}

