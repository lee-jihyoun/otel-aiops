package com.kt.springotellistener;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.scheduling.annotation.EnableScheduling;

@EnableScheduling
@SpringBootApplication
public class SpringOtelListenerApplication {

    public static void main(String[] args) {
        SpringApplication.run(SpringOtelListenerApplication.class, args);
    }

}
