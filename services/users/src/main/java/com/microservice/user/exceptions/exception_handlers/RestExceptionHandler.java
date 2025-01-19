package com.microservice.user.exceptions.exception_handlers;

import com.microservice.user.exceptions.not_found.UserNotFoundException;
import com.microservice.user.exceptions.null_property.NullUserException;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.ControllerAdvice;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.servlet.mvc.method.annotation.ResponseEntityExceptionHandler;

@ControllerAdvice
public class RestExceptionHandler extends ResponseEntityExceptionHandler {

  // These exceptions are usually raised when the "getSomethingById" methods
  // return null.
  // They imply that the requested object does not exist in the database, hence
  // causing the request
  // to fail gracefully.
  @ExceptionHandler({UserNotFoundException.class})
  public ResponseEntity<Object> handleNotFoundExceptions(RuntimeException exception) {
    return ResponseHandler.generateResponse(exception.getMessage(), HttpStatus.NOT_FOUND, null);
  }

  // These exceptions occur as a result of properties of entities being null, even
  // though they should not.
  // These exceptions usually imply an error with internal implementation and can
  // be deterimental.
  @ExceptionHandler({NullUserException.class})
  public ResponseEntity<Object> handleNullPropertyExceptions(RuntimeException exception) {
    String message = "An error has occurred. Please try again later.";
    return ResponseHandler.generateResponse(message, HttpStatus.INTERNAL_SERVER_ERROR, null);
  }
}
