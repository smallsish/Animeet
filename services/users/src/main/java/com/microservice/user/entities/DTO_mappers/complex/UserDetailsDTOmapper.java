package com.microservice.user.entities.DTO_mappers.complex;

import com.microservice.user.entities.DTO_mappers.simple.UserDTOmapper;
import com.microservice.user.entities.DTOs.complex.UserDetailsDTO;
import com.microservice.user.entities.DTOs.simple.UserDTO;
import com.microservice.user.entities.User;
import java.util.function.Function;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

@Component
public class UserDetailsDTOmapper implements Function<User, UserDetailsDTO> {

  @Autowired private UserDTOmapper userDTOmapper;

  @Override
  public UserDetailsDTO apply(User user) {
    UserDTO userDTO = userDTOmapper.apply(user);
    return new UserDetailsDTO(userDTO, user.getEmail(), user.getDateOfBirth());
  }
}
