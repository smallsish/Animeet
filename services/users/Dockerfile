# Step 1: Build stage
FROM maven:3.8.4-openjdk-17-slim AS build
WORKDIR /usr/src/app
COPY pom.xml .             
COPY src ./src

# Package the application without running tests
RUN mvn clean package -DskipTests

# Step 2: Runtime stage
FROM openjdk:17-jdk-slim
WORKDIR /usr/src/app
COPY --from=build /usr/src/app/target/user-0.0.1-SNAPSHOT.jar /usr/src/app/user-service.jar  
EXPOSE 5000                 
ENTRYPOINT ["java", "-jar", "/usr/src/app/user-service.jar"]
