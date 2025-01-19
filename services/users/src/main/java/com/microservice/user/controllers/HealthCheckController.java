package com.microservice.user.controllers;

import java.net.InetAddress;
import java.net.UnknownHostException;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class HealthCheckController {

  @GetMapping("/health")
  public HealthResponse health() {
    String ipAddress = getIpAddress();
    return new HealthResponse(ipAddress, "Service is healthy", "users");
  }

  private String getIpAddress() {
    try {
      return InetAddress.getLocalHost().getHostAddress();
    } catch (UnknownHostException e) {
      return "Unknown";
    }
  }

  public static class HealthResponse {
    private final String ip_address;
    private final String message;
    private final String service;

    public HealthResponse(String ip_address, String message, String service) {
      this.ip_address = ip_address;
      this.message = message;
      this.service = service;
    }

    public String getIp_address() {
      return ip_address;
    }

    public String getMessage() {
      return message;
    }

    public String getService() {
      return service;
    }
  }
}
