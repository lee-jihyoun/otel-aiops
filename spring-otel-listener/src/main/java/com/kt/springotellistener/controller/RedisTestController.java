package com.kt.springotellistener.controller;

import com.kt.springotellistener.service.RedisService;
import com.kt.springotellistener.vo.MyData;
import lombok.AllArgsConstructor;
import org.springframework.web.bind.annotation.*;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

@AllArgsConstructor
@RestController
public class RedisTestController {

    RedisService redisService;

    @GetMapping("/set")
    public String setValue() {
        redisService.setValue("myKey", "myValue");
        return "Value set";
    }

    @GetMapping("/get")
    public String getValue() {
        return redisService.getValue("myKey");
    }

    @GetMapping("/hset")
    public String hsetValue() {
        redisService.hsetValue("myHash:"+"a123", "field1", "value1");
        return "Hash value set";
    }

    @GetMapping("/hget")
    public String hgetValue() {
        return redisService.hgetValue("myHash"+"a123", "field1");
    }

    // 데이터 저장
    //    @PostMapping("/save")
    // 데이터 저장 엔드포인트
    @PostMapping("/save")
    public String saveData(@RequestBody MyData myData) {
        redisService.saveData(myData.getId(), myData.getData());
        return "Data saved for ID: " + myData.getId();
    }

    // 데이터 조회 엔드포인트
    @GetMapping("/get/{id}")
    public List<Object> getData(@PathVariable String id) {
        return redisService.getData(id);
    }

}
