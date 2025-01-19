package com.microservice.user;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.junit.jupiter.api.Assertions.assertThrows;

import com.microservice.user.controllers.HealthCheckController;
import com.microservice.user.entities.User;
import com.microservice.user.exceptions.not_found.UserNotFoundException;
import com.microservice.user.repositories.UserRepository;
import java.sql.Date;
import java.util.List;
import org.junit.jupiter.api.*;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.test.web.client.TestRestTemplate;
import org.springframework.boot.testcontainers.service.connection.ServiceConnection;
import org.springframework.http.ResponseEntity;
import org.springframework.test.context.ActiveProfiles;
import org.springframework.transaction.annotation.Transactional;
import org.testcontainers.containers.MySQLContainer;
import org.testcontainers.junit.jupiter.Testcontainers;

@SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT)
@ActiveProfiles("test")
@Testcontainers
@TestInstance(TestInstance.Lifecycle.PER_CLASS)
public class UserIntegrationTests implements AutoCloseable {

  @Autowired private UserRepository userRepo;

  @Autowired private TestRestTemplate restTemplate;

  @org.testcontainers.junit.jupiter.Container @ServiceConnection
  private static final MySQLContainer<?> mysqlContainer = new MySQLContainer<>("mysql:8.1.0");

  // @BeforeAll
  // void setUp() {
  //     mysqlContainer.start();
  // }

  static {
    mysqlContainer.start();
  }

  @BeforeEach
  void init() {
    userRepo.save(new User(1L, "user1", "user1@example.com", Date.valueOf("1990-01-01")));
    userRepo.save(new User(2L, "user2", "user2@example.com", Date.valueOf("1991-01-01")));
  }

  @Test
  public void testHealthCheck() {
    ResponseEntity<HealthCheckController.HealthResponse> response =
        restTemplate.getForEntity("/health", HealthCheckController.HealthResponse.class);

    assertEquals(200, response.getStatusCode().value());
    assertNotNull(response.getBody());
    assertEquals("Service is healthy", response.getBody().getMessage());
    assertEquals("users", response.getBody().getService());
  }

  @Test
  @Transactional
  public void testListUsers() {
    List<User> users = userRepo.findAll();
    assertEquals(2, users.size());
  }

  @Test
  @Transactional
  public void testGetUserById_UserFound() {
    User user = userRepo.findById(1L).orElseThrow(() -> new UserNotFoundException(1L));
    assertEquals("user1", user.getUsername());
  }

  @Test
  @Transactional
  public void testGetUserById_UserNotFound() {
    assertThrows(
        UserNotFoundException.class,
        () -> {
          userRepo.findById(999L).orElseThrow(() -> new UserNotFoundException(999L));
        });
  }

  @AfterAll
  void tearDown() {
    mysqlContainer.stop();
  }

  @Override
  public void close() {
    if (mysqlContainer != null) {
      mysqlContainer.close();
    }
  }
}
