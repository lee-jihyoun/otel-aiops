package com.kt.springotellistener.controller;

import com.kt.springotellistener.util.DataParsingService;
import lombok.AllArgsConstructor;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;


/*
 * json으로 데이터 수신
 * application/json
 * */
@AllArgsConstructor
@RestController
@RequestMapping("/otlp/filtered/json")
public class OtlpHttpFilterJsonController {

    DataParsingService dataParsingService;


    @PostMapping("/v1/traces")
    public ResponseEntity<String> receiveTraces(@RequestBody byte[] body) {
        dataParsingService.commonDataParsing(body,"filtered_span.json");
        return new ResponseEntity<>("OTLP Data received successfully", HttpStatus.OK);
    }

    @PostMapping("/v1/logs")
    public ResponseEntity<String> receiveLogs(@RequestBody byte[] body) {
        dataParsingService.commonDataParsing(body,"filtered_logs.json");
        return new ResponseEntity<>("OTLP Logs received successfully", HttpStatus.OK);
    }



}

