package com.kt.springotellistener.util;

import com.fasterxml.jackson.databind.ObjectMapper;
import lombok.AllArgsConstructor;
import org.springframework.stereotype.Service;

import java.io.ByteArrayInputStream;
import java.io.ByteArrayOutputStream;
import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.time.Instant;
import java.time.ZoneId;
import java.time.ZonedDateTime;
import java.time.format.DateTimeFormatter;
import java.util.*;
import java.util.zip.GZIPInputStream;


@AllArgsConstructor
@Service
public class DataParsingService {

    FileUtil fileUtil;

    DataUtil dataUtil;



    //[31, -117, 8, 0, 0, 0, 0, 0, 0, -1, -44, 89, 125, 108, 29, -59,...중략]
    //데이터가 gzip 압축되어 있는 형태라고 함
    // 바로 파싱을 할수 없고 압축을 푼다음 파싱(디코딩)을 진행해야함
    // decompressGzip 메서드에서 압축 해제 후 파싱 진행
    // 압축을 풀지 않으면 InvalidProtocolBufferException 이 발생함
    //gzip 압축해제
    public byte[] decompressGzip(byte[] compressed) throws IOException {
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




    public void commonDataParsing(byte[] compressed, String fileName){
        String parsingData = "";
        try{
            byte[] decompressedBody = decompressGzip(compressed);
            parsingData = new String(decompressedBody, StandardCharsets.UTF_8);
            fileUtil.saveToFile(fileName, parsingData);
        }catch (Exception e){
            e.printStackTrace();
        }
    }


    public List<Map<String, Object>> jsonTracesDataParsing(byte[] compressed, String type){
        String parsingData = "";
        List<Map<String, Object>> spanParsingList=null;
        try{
            byte[] decompressedBody = decompressGzip(compressed);
            parsingData = new String(decompressedBody, StandardCharsets.UTF_8);
            Map<String,Object> map = dataUtil.parseJsonToMap(parsingData);
            spanParsingList = parseResourceSpan(map);

//            String trace = dataUtil.convertMapToJson(spanParsingList);
//            fileUtil.saveToFile("parsing_span.json", trace);

        }catch (Exception e){
            e.printStackTrace();
        }

        return spanParsingList;
    }

    public String jsonMetricsDataParsing(byte[] compressed){
        String parsingData = "";
        try{
            byte[] decompressedBody = decompressGzip(compressed);
            parsingData = new String(decompressedBody, StandardCharsets.UTF_8);
            fileUtil.metricsSaveToFile(parsingData);
        }catch (Exception e){
            e.printStackTrace();
        }

        return parsingData;
    }

    public List<Map<String, Object>>  jsonLogsDataParsing(byte[] compressed, String type){
        String parsingData = "";
        List<Map<String, Object>> logParsingList=null;
        try{
            byte[] decompressedBody = decompressGzip(compressed);
            parsingData = new String(decompressedBody, StandardCharsets.UTF_8);
            Map<String,Object> map = dataUtil.parseJsonToMap(parsingData);
            logParsingList =  parseResourceLogs(map);
        }catch (Exception e){
            e.printStackTrace();
        }

        return logParsingList;
    }



    public List<Map<String, Object>> parseResourceLogs(Map<String, Object> jsonData) {
        List<Map<String, Object>> parsedLogs = new ArrayList<>();

        // resourceLogs 배열을 가져옴
        List<Map<String, Object>> resourceLogs = (List<Map<String, Object>>) jsonData.get("resourceLogs");

        for (Map<String, Object> resourceLog : resourceLogs) {
            Map<String, Object> parsedLog = new HashMap<>();
            // resource에서 필요한 데이터 추출
            Map<String, Object> resource = (Map<String, Object>) resourceLog.get("resource");
            if (resource != null && resource.containsKey("attributes")) {
                List<Map<String, Object>> attributes = (List<Map<String, Object>>) resource.get("attributes");

                for (Map<String, Object> attribute : attributes) {
                    String key = (String) attribute.get("key");
                    Map<String, Object> value = (Map<String, Object>) attribute.get("value");

                    switch (key) {
                        case "container.id":
                            parsedLog.put("container.id", value.get("stringValue"));
                            break;
                        case "os.description":
                            parsedLog.put("os.description", value.get("stringValue"));
                            break;
                        case "process.command_line":
                            parsedLog.put("process.command_line", value.get("stringValue"));
                            break;
                        case "service.name":
                            parsedLog.put("service.name", value.get("stringValue"));
                            break;
                        case "service.code":
                            parsedLog.put("service.code", value.get("stringValue"));
                            break;
                        case "telemetry.sdk.language":
                            parsedLog.put("telemetry.sdk.language", value.get("stringValue"));
                            break;
                    }
                }
            }

            // scopeLogs와 logRecords에서 필요한 정보 추출
            List<Map<String, Object>> scopeLogs = (List<Map<String, Object>>) resourceLog.get("scopeLogs");
            if (scopeLogs != null) {
                for (Map<String, Object> scopeLog : scopeLogs) {
                    List<Map<String, Object>> logRecords = (List<Map<String, Object>>) scopeLog.get("logRecords");

                    if (logRecords != null) {
                        for (Map<String, Object> logRecord : logRecords) {
                            if (scopeLog.containsKey("scope")) {
                                parsedLog.put("scope", scopeLog.get("scope"));
                            }
                            if (logRecord.containsKey("observedTimeUnixNano")) {
                                parsedLog.put("observedTimeUnixNano", convertNanoToDatetime(logRecord.get("observedTimeUnixNano").toString()));
                            }
                            if (logRecord.containsKey("severityText")) {
                                parsedLog.put("logRecords_severityText", logRecord.get("severityText"));
                            }
                            if (logRecord.containsKey("body")) {
                                Map<String, Object> body = (Map<String, Object>) logRecord.get("body");
                                if (body != null && body.containsKey("stringValue")) {
                                    parsedLog.put("logRecords_body_stringValue", body.get("stringValue"));
                                }
                            }
                            if (logRecord.containsKey("traceId") && logRecord.get("traceId") != null) {
                                parsedLog.put("traceId", logRecord.get("traceId"));
                            }
                            if (logRecord.containsKey("attributes")) {

                                List<Map<String, Object>> attributes = (List<Map<String, Object>>) logRecord.get("attributes");
                                for (Map<String, Object> attribute : attributes) {
                                    String key = (String) attribute.get("key");
                                    Map<String, Object> value = (Map<String, Object>) attribute.get("value");
                                    switch (key) {
                                        case "exception.message":
                                            parsedLog.put("log.exception.message", value.get("stringValue"));
                                            break;
                                        case "exception.stacktrace":
                                            String stacktrace = (String) value.get("stringValue");
                                            String shortStackTrace = String.join(" ", Arrays.asList(stacktrace.split("\n")).subList(0, 2));
                                            parsedLog.put("log.exception.stacktrace", stacktrace);
                                            parsedLog.put("log.exception.stacktrace.short", shortStackTrace);
                                            break;
                                        case "exception.type":
                                            parsedLog.put("log.exception.type", value.get("stringValue"));
                                            break;
                                    }

                                }
                            }
                        }
                    }
                }
            }

            // 파싱된 로그를 리스트에 추가
            parsedLogs.add(parsedLog);
        }

        return parsedLogs;
    }

    public List<Map<String, Object>> parseResourceSpan(Map<String, Object> jsonData) {
        ObjectMapper objectMapper = new ObjectMapper();
        List<Map<String, Object>> parsedDataList = new ArrayList<>();

        try {
            // resourceSpans를 추출
            List<Map<String, Object>> resourceSpans = (List<Map<String, Object>>) jsonData.get("resourceSpans");

            for (Map<String, Object> resource : resourceSpans) {
                String serviceName = null;
                String serviceCode = null;
                String osType = null;

                // resource -> attributes에서 필요한 값 추출
                if (resource.containsKey("resource") && ((Map)resource.get("resource")).containsKey("attributes")) {
                    List<Map<String, Object>> attributes = (List<Map<String, Object>>) ((Map)resource.get("resource")).get("attributes");

                    for (Map<String, Object> attribute : attributes) {
                        if ("service.name".equals(attribute.get("key"))) {
                            serviceName = (String) ((Map)attribute.get("value")).get("stringValue");
                        }
                        if ("service.code".equals(attribute.get("key"))) {
                            serviceCode = (String) ((Map)attribute.get("value")).get("stringValue");
                        }
                        if ("os.type".equals(attribute.get("key"))) {
                            osType = (String) ((Map)attribute.get("value")).get("stringValue");
                        }
                    }
                }

                // scopeSpans를 파싱
                List<Map<String, Object>> scopeSpans = (List<Map<String, Object>>) resource.get("scopeSpans");

                for (Map<String, Object> scopeSpan : scopeSpans) {
                    List<Map<String, Object>> spans = (List<Map<String, Object>>) scopeSpan.get("spans");

                    for (Map<String, Object> span : spans) {
                        Map<String, Object> parsedInfo = new HashMap<>();
                        parsedInfo.put("service.name", serviceName);
                        parsedInfo.put("service.code", serviceCode);
                        parsedInfo.put("os.type", osType);
                        parsedInfo.put("traceId", span.get("traceId"));
                        parsedInfo.put("spanId", span.get("spanId"));
                        parsedInfo.put("name", span.get("name"));
                        parsedInfo.put("startTimeUnixNano", convertNanoToDatetime(span.get("startTimeUnixNano").toString()));
                        parsedInfo.put("endTimeUnixNano", convertNanoToDatetime(span.get("endTimeUnixNano").toString()));
                        parsedInfo.put("http.status_code", null);
                        parsedInfo.put("rpc.grpc.status_code", null);
                        parsedInfo.put("trace.exception.message", null);
                        parsedInfo.put("trace.exception.stacktrace", null);
                        parsedInfo.put("trace.exception.stacktrace.short", null);
                        parsedInfo.put("http.url", null);
                        parsedInfo.put("rpc.method", null);

                        parsedInfo.put("http.response.status_code", null);
                        parsedInfo.put("server.address", null);
                        parsedInfo.put("server.port", null);
                        parsedInfo.put("http.route", null);

                        // span -> attributes에서 필요한 값을 추출
                        List<Map<String, Object>> spanAttributes = (List<Map<String, Object>>) span.get("attributes");
                        if (spanAttributes != null && !spanAttributes.isEmpty()) {
                            for (Map<String, Object> attribute : spanAttributes) {
                                try {
                                    if ("http.status_code".equals(attribute.get("key")) && ((Map) attribute.get("value")).containsKey("intValue")) {
                                        parsedInfo.put("http.status_code", ((Map) attribute.get("value")).get("intValue"));
                                    }
                                    if ("rpc.grpc.status_code".equals(attribute.get("key"))) {
                                        parsedInfo.put("rpc.grpc.status_code", ((Map) attribute.get("value")).get("intValue"));
                                    }
                                    if ("http.url".equals(attribute.get("key"))) {
                                        parsedInfo.put("http.url", ((Map) attribute.get("value")).get("stringValue"));
                                    }
                                    if ("rpc.method".equals(attribute.get("key"))) {
                                        parsedInfo.put("rpc.method", ((Map) attribute.get("value")).get("stringValue"));
                                    }

                                    if ("http.response.status_code".equals(attribute.get("key"))) {
                                        parsedInfo.put("http.response.status_code", ((Map) attribute.get("value")).get("intValue"));
                                    }
                                    if ("server.address".equals(attribute.get("key"))) {
                                        parsedInfo.put("server.address", ((Map) attribute.get("value")).get("stringValue"));
                                    }
                                    if ("server.port".equals(attribute.get("key"))) {
                                        parsedInfo.put("server.port", ((Map) attribute.get("value")).get("intValue"));
                                    }
                                    if ("http.route".equals(attribute.get("key"))) {
                                        parsedInfo.put("http.route", ((Map) attribute.get("value")).get("stringValue"));
                                    }

                                } catch (Exception e) {
                                    System.err.println("Error parsing attribute: " + e.getMessage());
                                    continue;
                                }
                            }
                        }

                        // 이벤트에서 예외 메시지 및 스택 트레이스를 파싱
                        List<Map<String, Object>> events = (List<Map<String, Object>>) span.get("events");
                        if (events != null && !events.isEmpty()) {
                            for (Map<String, Object> event : events) {
                                List<Map<String, Object>> eventAttributes = (List<Map<String, Object>>) event.get("attributes");
                                if (eventAttributes != null && !eventAttributes.isEmpty()) {
                                    for (Map<String, Object> attribute : eventAttributes) {
                                        if ("exception.message".equals(attribute.get("key"))) {
                                            parsedInfo.put("trace.exception.message", ((Map) attribute.get("value")).get("stringValue"));
                                        }
                                        if ("exception.stacktrace".equals(attribute.get("key"))) {
                                            String stacktrace = (String) ((Map) attribute.get("value")).get("stringValue");
                                            parsedInfo.put("trace.exception.stacktrace", stacktrace);

                                            // 두 번째 줄까지만 파싱하여 저장
                                            String shortStackTrace = String.join(" ", Arrays.asList(stacktrace.split("\n")).subList(0, 2));
                                            parsedInfo.put("trace.exception.stacktrace.short", shortStackTrace);
                                        }
                                    }
                                }
                            }
                        }
                        // 최종 파싱된 데이터 리스트에 추가
                        parsedDataList.add(parsedInfo);
                    }
                }
            }
        } catch (Exception e) {
            System.err.println("Error parsing JSON: " + e.getMessage());
        }

        return parsedDataList;
    }

    public String convertNanoToDatetime(String strNanoTime) {
        long nanoTime = Long.parseLong(strNanoTime);
        long seconds = nanoTime / 1_000_000_000L;
        ZonedDateTime utcTime = Instant.ofEpochSecond(seconds).atZone(ZoneId.of("UTC"));
        ZonedDateTime kstTime = utcTime.withZoneSameInstant(ZoneId.of("Asia/Seoul"));
        return kstTime.format(DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss"));
    }


//    public String jsonTracesDataParsing(byte[] compressed ){
//        String parsingData = "";
//        try{
//            byte[] decompressedBody = decompressGzip(compressed);
//            parsingData = new String(decompressedBody, StandardCharsets.UTF_8);
//            fileUtil.tracesSaveToFile(parsingData);
//        }catch (Exception e){
//            e.printStackTrace();
//        }
//
//        return parsingData;
//    }
//
//    public String jsonMetricsDataParsing(byte[] compressed){
//        String parsingData = "";
//        try{
//            byte[] decompressedBody = decompressGzip(compressed);
//            parsingData = new String(decompressedBody, StandardCharsets.UTF_8);
//            fileUtil.metricsSaveToFile(parsingData);
//        }catch (Exception e){
//            e.printStackTrace();
//        }
//
//        return parsingData;
//    }
//
//    public String jsonLogsDataParsing(byte[] compressed){
//        String parsingData = "";
//        try{
//            byte[] decompressedBody = decompressGzip(compressed);
//            parsingData = new String(decompressedBody, StandardCharsets.UTF_8);
//            fileUtil.logsSaveToFile(parsingData);
//        }catch (Exception e){
//            e.printStackTrace();
//        }
//
//        return parsingData;
//    }
//
//
//    public String protoTracesDataParsing (byte[] compressed) {
//        String parsingData = "";
//        try {
//            byte[] decompressedBody = decompressGzip(compressed);
//            TracesData traces = TracesData.parseFrom(decompressedBody);
//            parsingData = traces.toString();
//            fileUtil.tracesSaveToFile(parsingData);
//        } catch (Exception e) {
//            e.printStackTrace();
//        }
//        return parsingData;
//    }
//
//    public String protoMetricsDataParsing(byte[] compressed) {
//        String parsingData = "";
//        try {
//            byte[] decompressedBody = decompressGzip(compressed);
//            MetricsData metrics = MetricsData.parseFrom(decompressedBody);
//            parsingData = metrics.toString();
//            fileUtil.metricsSaveToFile(parsingData);
//        } catch (Exception e) {
//            e.printStackTrace();
//        }
//        return parsingData;
//    }
//
//    public String protoLogsDataParsing(byte[] compressed) {
//        String parsingData = "";
//        try {
//            byte[] decompressedBody = decompressGzip(compressed);
//            LogsData logs = LogsData.parseFrom(decompressedBody);
//            parsingData = logs.toString();
//            fileUtil.logsSaveToFile(parsingData);
//        } catch (Exception e) {
//            e.printStackTrace();
//        }
//        return parsingData;
//    }
}
