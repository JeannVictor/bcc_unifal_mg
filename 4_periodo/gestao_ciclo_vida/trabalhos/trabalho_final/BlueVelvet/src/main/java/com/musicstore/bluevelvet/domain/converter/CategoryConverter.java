package com.musicstore.bluevelvet.domain.converter;

import com.musicstore.bluevelvet.api.request.CategoryRequest;
import com.musicstore.bluevelvet.api.response.CategoryResponse;
import com.musicstore.bluevelvet.infrastructure.entity.Category;

public class CategoryConverter {


    public static CategoryResponse toResponse(Category category) {
        return CategoryResponse.builder()
                .id(category.getId())
                .name(category.getName())
                .image(category.getImage())
                .enabled(category.getEnabled())
                .parentId(category.getParent() != null ? category.getParent().getId() : null)
                .parentName(category.getParent() != null ? category.getParent().getName() : null)
                .build();
    }

    public static CategoryResponse toResponseWithChildren(Category category) {
        CategoryResponse response = toResponse(category);

        if (category.getChildren() != null && !category.getChildren().isEmpty()) {
            response.setChildren(
                    category.getChildren().stream()
                            .map(CategoryConverter::toResponse)
                            .toList()
            );
        }

        return response;
    }

    public static Category convertToCategory(CategoryRequest request) {
        if (request == null) {
            return null;
        }

        Category category = new Category();
        category.setName(request.getName());
        category.setImage(request.getImage());
        category.setEnabled(request.getEnabled() != null ? request.getEnabled() : true);

        return category;
    }

}