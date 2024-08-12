package com.kt.board.controller;


import lombok.RequiredArgsConstructor;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;

import org.springframework.scheduling.annotation.Async;
import org.springframework.scheduling.annotation.EnableAsync;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.concurrent.CompletableFuture;
import java.util.concurrent.ExecutionException;
import java.util.concurrent.TimeUnit;
import java.util.concurrent.TimeoutException;

@RestController
@RequiredArgsConstructor
@RequestMapping("/user")
public class UserController {

    private static final Logger logger = LogManager.getLogger(UserController.class.getName());


    @GetMapping("/null")
    public String getUser() {
		testA();
        logger.info("### getUser log start");
        String a = null;
        a.charAt(10);
		testB();
        return a;
    }


	public String testA(){
		try{
			Thread.sleep(5000);
		}catch(Exception e){

		}

		return "testA success";
	}

    @GetMapping("/server")
    public String getUserServerTimeout() {
        logger.info("### getUser server start");
        try {
            // 비동기 호출 및 타임아웃 설정
            CompletableFuture<String> future = CompletableFuture.supplyAsync(() -> testB());
            return future.get(5, TimeUnit.SECONDS);
        } catch (TimeoutException e) {
            throw new RuntimeException("Request timeout");
        } catch (InterruptedException | ExecutionException e) {
            throw new RuntimeException("Server error");
        }
    }

    @Async
	public String testB(){
		try{
			Thread.sleep(5000);
		}catch(Exception e){

		}
		return "testB success";
	}
}
