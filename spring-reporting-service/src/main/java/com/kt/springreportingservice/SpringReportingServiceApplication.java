package com.kt.springreportingservice;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.scheduling.annotation.EnableScheduling;

@EnableScheduling
@SpringBootApplication
public class SpringReportingServiceApplication {

	public static void main(String[] args) {
		SpringApplication.run(SpringReportingServiceApplication.class, args);
	}

}
