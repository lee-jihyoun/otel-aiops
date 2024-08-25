package com.kt.springotellistener.config;

import io.swagger.v3.oas.models.Components;
import io.swagger.v3.oas.models.OpenAPI;
import io.swagger.v3.oas.models.info.Info;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class OpenAPIConfig {
    @Bean
    public OpenAPI openAPI() {
        Info info = new Info()
                .title("Otlp Http Listener API Document")
                .version("v0.1.0")
                .description("JSON or Protocol Buffers type receiver");
        return new OpenAPI()
                .components(new Components())
                .info(info);
    }
}