//package com.kt.springotellistener.controller;
//
//import com.kt.springotellistener.service.RedisService;
//import com.kt.springotellistener.vo.MyData;
//import lombok.AllArgsConstructor;
//import org.springframework.web.bind.annotation.*;
//
//import java.util.List;
//
//@AllArgsConstructor
//@RestController
//public class RedisTestController {
//
//    RedisService redisService;
//
//    @GetMapping("/set")
//    public String setValue() {
//        redisService.setValue("myKey", "myValue");
//        System.out.println("###set in");
//        return "Value set";
//    }
//
//    @GetMapping("/get")
//    public String getValue() {
//        System.out.println("### get in");
//        return redisService.getValue("myKey");
//    }
//
//    @GetMapping("/hset")
//    public String hsetValue() {
//        redisService.hsetValue("myHash:"+"a123", "field1", "value1");
//        return "Hash value set";
//    }
//
//    @GetMapping("/hget")
//    public String hgetValue() {
//        return redisService.hgetValue("myHash"+"a123", "field1");
//    }
//
//    // 데이터 저장
//    //    @PostMapping("/save")
//    // 데이터 저장
//    @PostMapping("/save")
//    public String saveData(@RequestBody MyData myData) {
//        redisService.saveData(myData.getId(), myData.getData());
//        return "Data saved for ID: " + myData.getId();
//    }
//
//    // 데이터 조회
//    @GetMapping("/get/list/{id}")
//    public List<Object> getListData(@PathVariable String id) {
//        return redisService.getListData(id);
//    }
//
//    // 데이터 조회
//    @GetMapping("/get/hash/{id}")
//    public Object getHashData(@PathVariable String id) {
//        return redisService.getHashData(id);
//    }
//
//}
