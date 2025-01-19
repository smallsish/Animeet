package com.microservice.user.entities.DTO_mappers.simple;

import com.microservice.user.entities.DTOs.simple.UserDTO;
import com.microservice.user.entities.User;
import java.util.function.Function;
import org.springframework.stereotype.Component;

@Component
public class UserDTOmapper implements Function<User, UserDTO> {

  @Override
  public UserDTO apply(User user) {
    return new UserDTO(user.getId(), user.getUsername());
  }
}
