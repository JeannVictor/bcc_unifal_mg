package com.musicstore.bluevelvet.web.controller;

import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;

@Controller
public class WebDashboardController {

    @GetMapping("/dashboard")
    public String showDashboard() {
        return "dashboard";
    }
}
