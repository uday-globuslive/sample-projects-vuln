package com.example.vulnerable;

import org.junit.Test;
import static org.junit.Assert.*;

public class AppTest {
    @Test
    public void testProcessUserInput() {
        String result = App.processUserInput("test");
        assertNotNull(result);
    }
}
