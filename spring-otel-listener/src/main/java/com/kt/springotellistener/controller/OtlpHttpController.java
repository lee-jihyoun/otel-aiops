package com.kt.springotellistener.controller;

import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import io.opentelemetry.proto.trace.v1.TracesData;
import io.opentelemetry.proto.logs.v1.LogsData;
import io.opentelemetry.proto.metrics.v1.MetricsData;

import java.io.ByteArrayInputStream;
import java.io.ByteArrayOutputStream;
import java.io.IOException;
import java.util.Arrays;
import java.util.zip.GZIPInputStream;

@RestController
@RequestMapping("/otlp")
public class OtlpHttpController {

    @PostMapping("/v1/traces")
    public ResponseEntity<String> receiveTraces(@RequestBody byte[] body) {
        System.out.println("Received OTLP HTTP binary trace data");
        System.out.println(Arrays.toString(body));
        //[31, -117, 8, 0, 0, 0, 0, 0, 0, -1, -44, 89, 125, 108, 29, -59,...중략]
        //데이터가 gzip 압축되어 있는 형태라고 함
        // 바로 파싱을 할수 없고 압축을 푼다음 파싱(디코딩)을 진행해야함
        // decompressGzip 메서드에서 압축 해제 후 파싱 진행
        // 압축을 풀지 않으면 InvalidProtocolBufferException 이 발생함
        try {
            //gzip 압축 해제
            byte[] decompressedBody = decompressGzip(body);
            //압축 해제 후 파싱
            TracesData traces = TracesData.parseFrom(decompressedBody);
            System.out.println("Decoded OTLP Trace Data: " + traces.toString());
        } catch (Exception e) {
            e.printStackTrace();
        }
        return new ResponseEntity<>("OTLP Data received successfully", HttpStatus.OK);
    }

    @PostMapping("/v1/metrics")
    public ResponseEntity<String> receiveMetrics(@RequestBody byte[] body) {
        System.out.println("Received OTLP HTTP binary metrics data");
        System.out.println(Arrays.toString(body));
        try {
            byte[] decompressedBody = decompressGzip(body);
            MetricsData metrics = MetricsData.parseFrom(decompressedBody);
            System.out.println("Decoded OTLP Metrics Data: " + metrics.toString());
        } catch (Exception e) {
            e.printStackTrace();
        }
        return new ResponseEntity<>("OTLP Metrics received successfully", HttpStatus.OK);
    }


    @PostMapping("/v1/logs")
    public ResponseEntity<String> receiveLogs(@RequestBody byte[] body) {
        System.out.println("Received OTLP HTTP binary logs data");
        System.out.println(Arrays.toString(body));
        try {
            byte[] decompressedBody = decompressGzip(body);
            LogsData logs = LogsData.parseFrom(decompressedBody);
            System.out.println("Decoded OTLP Log Data: " + logs.toString());
        } catch (Exception e) {
            e.printStackTrace();
        }
        return new ResponseEntity<>("OTLP Logs received successfully", HttpStatus.OK);
    }

    //gzip 압축해제
    private byte[] decompressGzip(byte[] compressed) throws IOException {
        try (ByteArrayInputStream byteStream = new ByteArrayInputStream(compressed);
             GZIPInputStream gzipStream = new GZIPInputStream(byteStream);
             ByteArrayOutputStream outStream = new ByteArrayOutputStream()) {
            byte[] buffer = new byte[1024];
            int len;
            while ((len = gzipStream.read(buffer)) > 0) {
                outStream.write(buffer, 0, len);
            }
            return outStream.toByteArray();
        }
    }

}

