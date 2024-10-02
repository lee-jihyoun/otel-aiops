package com.kt.springotellistener.controller;

import com.kt.springotellistener.service.RedisService;
import com.kt.springotellistener.util.DataParsingService;
import lombok.AllArgsConstructor;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;
import java.util.Map;


/*
 * json으로 데이터 수신
 * application/json
 * */
@AllArgsConstructor
@RestController
@RequestMapping("/otlp/filtered/json")
public class OtlpHttpFilterJsonController {

    DataParsingService dataParsingService;

    RedisService redisService;

//filtered_trace_hash filtered_log_hash key_store
    @PostMapping("/v1/traces")
    public ResponseEntity<String> receiveTraces(@RequestBody byte[] body) {
        List<Map<String,Object>> traceList = dataParsingService.jsonTracesDataParsing(body,"filtered_span");
        redisService.saveToRedis("filtered_trace",traceList);
        return new ResponseEntity<>("OTLP Data received successfully", HttpStatus.OK);
    }

    @PostMapping("/v1/logs")
    public ResponseEntity<String> receiveLogs(@RequestBody byte[] body) {
        List<Map<String,Object>> logList = dataParsingService.jsonLogsDataParsing(body,"filtered_logs");
        redisService.saveToRedis("filtered_log",logList);
        return new ResponseEntity<>("OTLP Logs received successfully", HttpStatus.OK);
    }



}

