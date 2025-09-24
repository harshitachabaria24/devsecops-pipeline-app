package com.example.devsecopsapp;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

@SpringBootApplication
public class DevsecopsAppApplication {
    public static void main(String[] args) {
        SpringApplication.run(DevsecopsAppApplication.class, args);
    }
}

@RestController
class HealthController {
    @GetMapping("/health")
    public String healthCheck() {
        return "App is running OK!";
    }
}
