package com.coinconverter.CoinConverter.entity;

import jakarta.persistence.*;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Getter;
import lombok.NoArgsConstructor;
import org.hibernate.annotations.CreationTimestamp;

import java.io.Serializable;
import java.math.BigDecimal;
import java.time.LocalDateTime;

@Entity
@Getter
@Builder
@NoArgsConstructor
@AllArgsConstructor
@Table(name = "conversions")
public class Conversion implements Serializable {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(name = "from_coin", nullable = false, length = 3)
    private String fromCoin;

    @Column(name = "to_coin", nullable = false, length = 3)
    private String toCoin;

    @Column(precision = 19, scale = 6)
    private BigDecimal amount;

    @Column(precision = 19, scale = 6)
    private BigDecimal rate;

    @Column(precision = 19, scale = 6)
    private BigDecimal convertedAmount;

    @CreationTimestamp
    @Column(name = "converted_at", nullable = false, updatable = false)
    private LocalDateTime convertedDateTime;

    @Column(name = "user_email")
    private String userEmail;
}
