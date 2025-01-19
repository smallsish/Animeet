package com.microservice.user.controllers;

import com.microservice.user.entities.DTO_mappers.complex.UserDetailsDTOmapper;
import com.microservice.user.entities.DTO_mappers.simple.UserDTOmapper;
import com.microservice.user.entities.DTOs.complex.UserDetailsDTO;
import com.microservice.user.entities.DTOs.simple.UserDTO;
import com.microservice.user.entities.User;
import com.microservice.user.exceptions.not_found.UserNotFoundException;
import com.microservice.user.services.UserService;
import java.util.List;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.ResponseStatus;
import org.springframework.web.bind.annotation.RestController;

@RestController
@CrossOrigin // Enable CORS for this controller
public class UserController {

  private final UserService userService;
  private final UserDTOmapper userDTOmapper;
  private final UserDetailsDTOmapper userDetailsDTOmapper;

  // Constructor Injection
  public UserController(
      UserService userService,
      UserDTOmapper userDTOmapper,
      UserDetailsDTOmapper userDetailsDTOmapper) {
    this.userService = userService;
    this.userDTOmapper = userDTOmapper;
    this.userDetailsDTOmapper = userDetailsDTOmapper;
  }
  /**
   * List all users in the system
   *
   * @return list of all users (mapped to basic DTO)
   */
  @ResponseStatus(HttpStatus.OK)
  @GetMapping("/users")
  public List<UserDTO> getUsers() {
    List<User> users = userService.listUsers();

    if (userDTOmapper == null) {
      throw new RuntimeException("UserDTOMapper is null");
    }

    return users.stream().map(userDTOmapper).toList();
  }

  /**
   * Search for user with the given id If there is no user with the given "id", throw a
   * UserNotFoundException
   *
   * @param id
   * @return User with the given id, with confidential details (mapped to detailed DTO)
   */
  @ResponseStatus(HttpStatus.OK)
  @GetMapping("/users/{id}")
  public UserDetailsDTO getUserDetails(@PathVariable Long id) {
    User user = userService.getUserById(id);
    if (user == null) throw new UserNotFoundException(id);
    return userDetailsDTOmapper.apply(user);
  }
}
