//package com.kt.springotellistener.controller;
//
//import com.kt.springotellistener.util.DataParsingService;
//import lombok.AllArgsConstructor;
//import org.springframework.http.HttpStatus;
//import org.springframework.http.ResponseEntity;
//import org.springframework.web.bind.annotation.PostMapping;
//import org.springframework.web.bind.annotation.RequestBody;
//import org.springframework.web.bind.annotation.RequestMapping;
//import org.springframework.web.bind.annotation.RestController;
//
//
///*
//* Protocol Buffers 데이터 수신
//* application/x-protobuf
//* */
//@AllArgsConstructor
//@RestController
//@RequestMapping("/otlp/protobuf")
//public class OtlpHttpProtobufController {
//
//    DataParsingService dataParsingService;
//
//    @PostMapping("/v1/traces")
//    public ResponseEntity<String> receiveTraces(@RequestBody byte[] body) {
//        dataParsingService.protoTracesDataParsing(body);
//        return new ResponseEntity<>("OTLP Data received successfully", HttpStatus.OK);
//    }
//
//
//    //애로 다 다시개발해야함
//    @PostMapping("/v1/metrics")
//    public ResponseEntity<String> receiveMetrics(@RequestBody byte[] body) {
//        dataParsingService.protoMetricsDataParsing(body);
//        return new ResponseEntity<>("OTLP Metrics received successfully", HttpStatus.OK);
//    }
//
//
//    @PostMapping("/v1/logs")
//    public ResponseEntity<String> receiveLogs(@RequestBody byte[] body) {
//        dataParsingService.protoLogsDataParsing(body);
//        return new ResponseEntity<>("OTLP Logs received successfully", HttpStatus.OK);
//    }
//
//
//
//}
//
