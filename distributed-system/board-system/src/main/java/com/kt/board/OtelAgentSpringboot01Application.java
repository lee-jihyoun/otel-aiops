package com.kt.board;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.boot.builder.SpringApplicationBuilder;
import org.springframework.boot.web.servlet.support.SpringBootServletInitializer;

@SpringBootApplication
public class OtelAgentSpringboot01Application extends SpringBootServletInitializer {


	public static void main(String[] args) {
		SpringApplication.run(OtelAgentSpringboot01Application.class, args);
	}

	@Override
	protected SpringApplicationBuilder configure(SpringApplicationBuilder application) {
		return super.configure(application);
	}

}
