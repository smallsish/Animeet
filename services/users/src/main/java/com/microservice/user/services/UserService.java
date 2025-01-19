package com.microservice.user.services;

import com.microservice.user.entities.User;
import java.util.List;

public interface UserService {

  List<User> listUsers();

  User getUserById(Long id);
}
