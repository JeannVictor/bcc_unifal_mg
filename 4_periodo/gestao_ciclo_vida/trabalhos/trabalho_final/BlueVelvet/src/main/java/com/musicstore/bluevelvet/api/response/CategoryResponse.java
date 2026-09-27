package com.musicstore.bluevelvet.api.response;

import com.fasterxml.jackson.annotation.JsonInclude;
import lombok.*;

import java.util.List;

@Getter
@Setter
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class CategoryResponse {

    private Long id;

    private String name;

    private String image;

    private Boolean enabled;

    //  Informações sobre o parent
    private Long parentId;
    private String parentName;

    //  Subcategorias
    @JsonInclude(JsonInclude.Include.NON_EMPTY)
    private List<CategoryResponse> children;
}