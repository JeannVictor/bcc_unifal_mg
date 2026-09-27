package com.musicstore.bluevelvet.api.response;

import com.musicstore.bluevelvet.domain.enums.UserRole;
import lombok.*;

@Getter
@Setter
@Builder
@ToString
@NoArgsConstructor
@AllArgsConstructor
public class AuthResponse {

    private Long id;
    private String email;
    private UserRole role;
    private String message;
}
