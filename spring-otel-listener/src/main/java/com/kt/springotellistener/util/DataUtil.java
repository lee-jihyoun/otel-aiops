package com.kt.springotellistener.util;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.springframework.stereotype.Component;

import java.util.List;
import java.util.Map;


@Component
public class DataUtil {

    // string 데이터를 map으로 변환
    public Map<String, Object> parseJsonToMap(String jsonData) {
        ObjectMapper objectMapper = new ObjectMapper();
        Map<String, Object> resultMap = null;
        try {
            resultMap = objectMapper.readValue(jsonData, Map.class);
        } catch (Exception e) {
            e.printStackTrace();
        }
        return resultMap;
    }

    //map 데이터를 json으로변환
    public String convertMapToJson(Map<String, Object> data) {
        ObjectMapper objectMapper = new ObjectMapper();
        String json="";
        try {
            json = objectMapper.writeValueAsString(data);
//            System.out.println(json);
        } catch (JsonProcessingException e) {
            e.printStackTrace();
        }
        return json;
    }

    public String convertListToString(List<Map<String, Object>> list){
        ObjectMapper objectMapper = new ObjectMapper();
        String resultString="";
        try{
            resultString= objectMapper.writeValueAsString(list);
        }catch (Exception e){

        }
        return resultString;
    }
}
