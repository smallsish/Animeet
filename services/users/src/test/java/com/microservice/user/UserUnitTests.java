package com.microservice.user;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.*;

import com.microservice.user.controllers.UserController;
import com.microservice.user.entities.DTO_mappers.complex.UserDetailsDTOmapper;
import com.microservice.user.entities.DTO_mappers.simple.UserDTOmapper;
import com.microservice.user.entities.DTOs.complex.UserDetailsDTO;
import com.microservice.user.entities.DTOs.simple.UserDTO;
import com.microservice.user.entities.User;
import com.microservice.user.exceptions.not_found.UserNotFoundException;
import com.microservice.user.services.UserService;
import java.sql.Date;
import java.util.Arrays;
import java.util.List;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.MockitoAnnotations;

public class UserUnitTests {

  @Mock private UserService userService;

  @Mock private UserDTOmapper userDTOmapper;

  @Mock private UserDetailsDTOmapper userDetailsDTOmapper;

  @InjectMocks private UserController userController;

  @BeforeEach
  public void setUp() {
    MockitoAnnotations.openMocks(this);
  }

  @Test
  public void testGetUsers() {
    User user1 =
        User.builder()
            .id(1L)
            .username("user1")
            .email("user1@example.com")
            .dateOfBirth(Date.valueOf("1990-01-01"))
            .build();

    User user2 =
        User.builder()
            .id(2L)
            .username("user2")
            .email("user2@example.com")
            .dateOfBirth(Date.valueOf("1991-01-01"))
            .build();

    UserDTO userDTO1 = new UserDTO(1L, "user1");
    UserDTO userDTO2 = new UserDTO(2L, "user2");

    when(userService.listUsers()).thenReturn(Arrays.asList(user1, user2));
    when(userDTOmapper.apply(user1)).thenReturn(userDTO1);
    when(userDTOmapper.apply(user2)).thenReturn(userDTO2);

    List<UserDTO> result = userController.getUsers();

    assertEquals(2, result.size());
    assertEquals(userDTO1, result.get(0));
    assertEquals(userDTO2, result.get(1));
    verify(userService).listUsers();
    verify(userDTOmapper, times(2)).apply(any(User.class));
  }

  @Test
  public void testGetUserDetails_UserFound() {
    Long userId = 1L;
    User user =
        User.builder()
            .id(userId)
            .username("user1")
            .email("user1@example.com")
            .dateOfBirth(Date.valueOf("1990-01-01"))
            .build();

    UserDetailsDTO userDetailsDTO =
        new UserDetailsDTO(
            new UserDTO(userId, "user1"), "user1@example.com", Date.valueOf("1990-01-01"));

    when(userService.getUserById(userId)).thenReturn(user);
    when(userDetailsDTOmapper.apply(user)).thenReturn(userDetailsDTO);

    UserDetailsDTO result = userController.getUserDetails(userId);

    assertNotNull(result);
    assertEquals(userDetailsDTO, result);
    verify(userService).getUserById(userId);
    verify(userDetailsDTOmapper).apply(user);
  }

  @Test
  public void testGetUserDetails_UserNotFound() {
    Long userId = 1L;
    when(userService.getUserById(userId)).thenReturn(null);

    assertThrows(UserNotFoundException.class, () -> userController.getUserDetails(userId));
    verify(userService).getUserById(userId);
  }
}
