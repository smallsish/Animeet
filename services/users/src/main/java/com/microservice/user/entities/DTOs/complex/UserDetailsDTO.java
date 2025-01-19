package com.microservice.user.entities.DTOs.complex;

import com.microservice.user.entities.DTOs.simple.UserDTO;
import java.sql.Date;
import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;

@Getter
@AllArgsConstructor
@NoArgsConstructor
public class UserDetailsDTO {
  private UserDTO user;
  private String email;
  private Date dateOfBirth;
}
