package com.example.vulnerable;

import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.apache.http.client.HttpClient;
import org.apache.http.impl.client.HttpClients;
import java.io.IOException;

/**
 * Vulnerable Java Application using Gradle
 * Contains intentional vulnerabilities for demonstration
 */
public class GradleApp {
    private static final Logger logger = LogManager.getLogger(GradleApp.class);
    private static final ObjectMapper objectMapper = new ObjectMapper();

    public static void main(String[] args) {
        System.out.println("Gradle Vulnerable Application");
        
        // Demonstrates use of vulnerable log4j
        logger.info("Application started");
        
        // Vulnerable HTTP client
        HttpClient httpClient = HttpClients.createDefault();
        logger.info("HTTP Client created");
        
        // Vulnerable Jackson deserialization
        try {
            objectMapper.enableDefaultTyping();
            String json = "{\"@class\": \"java.lang.ProcessBuilder\"}";
            Object obj = objectMapper.readValue(json, Object.class);
            logger.info("Deserialized object: " + obj);
        } catch (IOException e) {
            logger.error("Error in deserialization", e);
        }
        
        // Vulnerable string interpolation
        String userInput = "${java.version}";
        logger.warn("Processing user input: " + userInput);
    }
    
    /**
     * Vulnerable method with SQL injection potential
     */
    public static String executeQuery(String tableName) {
        // No parameterization - vulnerable to SQL injection
        return "SELECT * FROM " + tableName;
    }
    
    /**
     * Vulnerable method with command execution potential
     */
    public static void runCommand(String cmd) throws IOException {
        // Dangerous - vulnerable to command injection
        Runtime.getRuntime().exec(cmd);
    }
}
