package com.kt.board.controller;


import lombok.RequiredArgsConstructor;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequiredArgsConstructor
@RequestMapping("/user")
public class UserController {

    private static final Logger logger = LogManager.getLogger(UserController.class.getName());


    @GetMapping("")
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
	
	public String testB(){
		try{
			Thread.sleep(5000);			
		}catch(Exception e){
			
		}
		return "testB success";
	}
}
