package com.example.vulnerable;

import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import com.fasterxml.jackson.databind.ObjectMapper;
import java.io.IOException;

/**
 * Vulnerable Java Application for SCA Scanning
 * Contains intentional vulnerabilities for demonstration
 */
public class App {
    private static final Logger logger = LogManager.getLogger(App.class);
    private static final ObjectMapper objectMapper = new ObjectMapper();

    public static void main(String[] args) {
        System.out.println("Maven Vulnerable Application");
        
        // Demonstrates use of vulnerable log4j
        logger.info("Application started");
        
        // Vulnerable deserialization example
        try {
            String json = "{\"class\": \"java.lang.Runtime\"}";
            Object obj = objectMapper.readValue(json, Object.class);
            logger.info("JSON deserialized: " + obj);
        } catch (IOException e) {
            logger.error("Error deserializing JSON", e);
        }
        
        // Vulnerable string processing
        String userInput = "${7*7}";
        logger.info("User input: " + userInput);
    }
    
    /**
     * Vulnerable method that doesn't validate input
     */
    public static String processUserInput(String input) {
        // No validation - vulnerable to injection
        return "Processing: " + input;
    }
}
