package com.example.vulnerable;

import org.junit.Test;
import static org.junit.Assert.*;

public class GradleAppTest {
    @Test
    public void testExecuteQuery() {
        String result = GradleApp.executeQuery("users");
        assertNotNull(result);
        assertTrue(result.contains("users"));
    }
    
    @Test
    public void testAppStarts() {
        // Simple test
        assertNotNull(GradleApp.class);
    }
}
