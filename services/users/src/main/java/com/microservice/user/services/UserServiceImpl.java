package com.microservice.user.services;

import com.microservice.user.entities.User;
import com.microservice.user.exceptions.not_found.UserNotFoundException;
import com.microservice.user.repositories.UserRepository;
import java.util.List;
import java.util.Optional;
import org.springframework.stereotype.Service;

@Service
public class UserServiceImpl implements UserService {

  private UserRepository userRepo;

  public UserServiceImpl(UserRepository userRepo) {
    this.userRepo = userRepo;
  }

  /**
   * Get all Users
   *
   * @return A list of all Users
   */
  @Override
  public List<User> listUsers() {
    return userRepo.findAll();
  }

  /**
   * Get the User with the specified id
   *
   * @param userId
   * @return The User with the specified id
   * @throws UserNotFoundException If a User with the specified id does not exist
   */
  @Override
  public User getUserById(Long userId) {
    Optional<User> user = userRepo.findById(userId);
    if (user.isEmpty()) {
      throw new UserNotFoundException(userId);
    }

    return user.get();
  }
}
