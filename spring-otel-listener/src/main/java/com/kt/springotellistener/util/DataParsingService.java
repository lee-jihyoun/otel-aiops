package com.kt.springotellistener.util;

import io.opentelemetry.proto.logs.v1.LogsData;
import io.opentelemetry.proto.metrics.v1.MetricsData;
import io.opentelemetry.proto.trace.v1.TracesData;
import lombok.AllArgsConstructor;
import org.springframework.stereotype.Service;

import java.io.ByteArrayInputStream;
import java.io.ByteArrayOutputStream;
import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.util.zip.GZIPInputStream;


@AllArgsConstructor
@Service
public class DataParsingService {

    FileUtil fileUtil;

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


    public String jsonTracesDataParsing(byte[] compressed ){
        String parsingData = "";
        try{
            byte[] decompressedBody = decompressGzip(compressed);
            parsingData = new String(decompressedBody, StandardCharsets.UTF_8);
            fileUtil.tracesSaveToFile(parsingData);
        }catch (Exception e){
            e.printStackTrace();
        }

        return parsingData;
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

    public String jsonLogsDataParsing(byte[] compressed){
        String parsingData = "";
        try{
            byte[] decompressedBody = decompressGzip(compressed);
            parsingData = new String(decompressedBody, StandardCharsets.UTF_8);
            fileUtil.logsSaveToFile(parsingData);
        }catch (Exception e){
            e.printStackTrace();
        }

        return parsingData;
    }


    public String protoTracesDataParsing (byte[] compressed) {
        String parsingData = "";
        try {
            byte[] decompressedBody = decompressGzip(compressed);
            TracesData traces = TracesData.parseFrom(decompressedBody);
            parsingData = traces.toString();
            fileUtil.tracesSaveToFile(parsingData);
        } catch (Exception e) {
            e.printStackTrace();
        }
        return parsingData;
    }

    public String protoMetricsDataParsing(byte[] compressed) {
        String parsingData = "";
        try {
            byte[] decompressedBody = decompressGzip(compressed);
            MetricsData metrics = MetricsData.parseFrom(decompressedBody);
            parsingData = metrics.toString();
            fileUtil.metricsSaveToFile(parsingData);
        } catch (Exception e) {
            e.printStackTrace();
        }
        return parsingData;
    }

    public String protoLogsDataParsing(byte[] compressed) {
        String parsingData = "";
        try {
            byte[] decompressedBody = decompressGzip(compressed);
            LogsData logs = LogsData.parseFrom(decompressedBody);
            parsingData = logs.toString();
            fileUtil.logsSaveToFile(parsingData);
        } catch (Exception e) {
            e.printStackTrace();
        }
        return parsingData;
    }
}
