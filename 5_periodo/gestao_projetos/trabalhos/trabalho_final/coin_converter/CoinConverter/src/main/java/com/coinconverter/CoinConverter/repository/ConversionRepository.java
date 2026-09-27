package com.coinconverter.CoinConverter.repository;

import com.coinconverter.CoinConverter.entity.Conversion;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.time.LocalDateTime;
import java.util.List;
import java.util.Map;

@Repository
public interface ConversionRepository extends JpaRepository<Conversion, Long> {

    // TODO: USER-RELATED QUERIES (REQUIRE USER TO BE LOGGED IN)

    // Logged-in user views their conversion history in descending order
    List<Conversion> findAllByUserEmailOrderByIdDesc(String userEmail);

    @Query(value = "SELECT " +
            "from_coin, " +
            "to_coin, " +
            "CONCAT(from_coin, ' -> ', to_coin) as conversion_pair, " +
            "COUNT(*) as total_conversions, " +
            "ROUND((COUNT(*) * 100.0 / SUM(COUNT(*)) OVER ()), 2) as total_percentage " +
            "FROM conversions " +
            "WHERE (:begin IS NULL OR converted_at >= :begin) " +
            "AND (user_email = :userEmail) " +
            "AND (:end IS NULL OR converted_at <=  :end) " +
            "GROUP BY from_coin, to_coin " +
            "ORDER BY total_conversions DESC " +
            "LIMIT :limit",
            nativeQuery = true)
    List<Map<String, Object>> findTopConversionsByUser(@Param("userEmail") String userEmail, @Param("limit") int limit,
                                                       @Param("begin") LocalDateTime begin, @Param("end") LocalDateTime end);

    // Logged-in user views the most used source currencies within a period or all time
    @Query(value = "SELECT " +
            "from_coin, " +
            "COUNT(*) as total_conversions, " +
            "ROUND((COUNT(*) * 100.0 / SUM(COUNT(*)) OVER ()), 2) as total_percentage " +
            "FROM conversions " +
            "WHERE (:begin IS NULL OR converted_at >= :begin) " +
            "AND (user_email = :userEmail) " +
            "AND (:end IS NULL OR converted_at <=  :end) " +
            "GROUP BY from_coin " +
            "ORDER BY total_conversions DESC " +
            "LIMIT :limit",
            nativeQuery = true)
    List<Map<String, Object>> findTopFromCoinsConversionsByUser(@Param("userEmail") String userEmail, @Param("limit") int limit,
                                                                @Param("begin") LocalDateTime begin, @Param("end") LocalDateTime end);

    // Logged-in user views the most used target currencies
    @Query(value = "SELECT " +
            "to_coin, " +
            "COUNT(*) as total_conversions, " +
            "ROUND((COUNT(*) * 100.0 / SUM(COUNT(*)) OVER ()), 2) as total_percentage " +
            "FROM conversions " +
            "WHERE (:begin IS NULL OR converted_at >= :begin) " +
            "AND (user_email = :userEmail) " +
            "AND (:end IS NULL OR converted_at <=  :end) " +
            "GROUP BY to_coin " +
            "ORDER BY total_conversions DESC " +
            "LIMIT :limit",
            nativeQuery = true)
    List<Map<String, Object>> findTopToCoinsConversionsByUser(@Param("userEmail") String userEmail, @Param("limit") int limit,
                                                              @Param("begin") LocalDateTime begin, @Param("end") LocalDateTime end);


    // TODO: NON-USER-RELATED QUERIES (USER MAY BE LOGGED IN OR NOT)

    // User (logged in or not) views the top "N" most frequent conversions within a period or all time
    @Query(value = "SELECT " +
            "from_coin, " +
            "to_coin, " +
            "CONCAT(from_coin, ' -> ', to_coin) as conversion_pair, " +
            "COUNT(*) as total_conversions, " +
            "ROUND((COUNT(*) * 100.0 / SUM(COUNT(*)) OVER ()), 2) as total_percentage " +
            "FROM conversions " +
            "WHERE (:begin IS NULL OR converted_at >= :begin) " +
            "AND (:end IS NULL OR converted_at <=  :end) " +
            "GROUP BY from_coin, to_coin " +
            "ORDER BY total_conversions DESC " +
            "LIMIT :limit",
            nativeQuery = true)
    List<Map<String, Object>> findTopConversions(@Param("limit") int limit, @Param("begin") LocalDateTime begin, @Param("end") LocalDateTime end);

    // User (logged in or not) views the most used source currencies within a period or all time
    @Query(value = "SELECT " +
            "from_coin, " +
            "COUNT(*) as total_conversions, " +
            "ROUND((COUNT(*) * 100.0 / SUM(COUNT(*)) OVER ()), 2) as total_percentage " +
            "FROM conversions " +
            "WHERE (:begin IS NULL OR converted_at >= :begin) " +
            "AND (:end IS NULL OR converted_at <=  :end) " +
            "GROUP BY from_coin " +
            "ORDER BY total_conversions DESC " +
            "LIMIT :limit",
            nativeQuery = true)
    List<Map<String, Object>> findTopFromCoinsConversions(@Param("limit") int limit, @Param("begin") LocalDateTime begin, @Param("end") LocalDateTime end);

    // User (logged in or not) views the most used target currencies
    @Query(value = "SELECT " +
            "to_coin, " +
            "COUNT(*) as total_conversions, " +
            "ROUND((COUNT(*) * 100.0 / SUM(COUNT(*)) OVER ()), 2) as total_percentage " +
            "FROM conversions " +
            "WHERE (:begin IS NULL OR converted_at >= :begin) " +
            "AND (:end IS NULL OR converted_at <=  :end) " +
            "GROUP BY to_coin " +
            "ORDER BY total_conversions DESC " +
            "LIMIT :limit",
            nativeQuery = true)
    List<Map<String, Object>> findTopToCoinsConversions(@Param("limit") int limit, @Param("begin") LocalDateTime begin, @Param("end") LocalDateTime end);

    // User (logged in or not) views the latest conversions globally
    @Query(value = "SELECT * FROM conversions ORDER BY id DESC LIMIT :limit", nativeQuery = true)
    List<Conversion> findLastConversions(@Param("limit") int limit);
}