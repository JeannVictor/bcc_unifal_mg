package com.musicstore.bluevelvet.infrastructure.repository;

import com.musicstore.bluevelvet.infrastructure.entity.Category;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.Optional;

@Repository
public interface CategoryRepository extends JpaRepository<Category, Long> {

    Optional<Category> findByName(String name);
    boolean existsByName(String name);

    Page<Category> findByEnabledTrue(Pageable pageable);
    List<Category> findByEnabledTrueOrderByNameAsc();

    Page<Category> findByParentIsNull(Pageable pageable);
    List<Category> findByParentIsNullAndEnabledTrue();

    List<Category> findByParentId(Long parentId);
    boolean existsByParentId(Long parentId);

    Page<Category> findByNameContainingIgnoreCase(String name, Pageable pageable);

    List<Category> findAllByOrderByNameAsc();
}