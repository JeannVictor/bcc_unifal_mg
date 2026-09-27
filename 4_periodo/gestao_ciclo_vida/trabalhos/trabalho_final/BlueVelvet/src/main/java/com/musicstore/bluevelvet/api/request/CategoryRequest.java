package com.musicstore.bluevelvet.api.request;

import lombok.*;

@Getter
@Setter
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class CategoryRequest {

    private String name;
    private String image;
    private Boolean enabled;
    private Long parentId;
}
