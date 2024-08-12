package com.kt;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;

import java.io.File;
import java.io.IOException;
import java.util.Iterator;

public class JsonParser {

    public static void main(String[] args) {
        try {
            ObjectMapper mapper = new ObjectMapper();
            JsonNode rootNode = mapper.readTree(new File("metrics.json"));
            parseJson("", rootNode);
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    private static void parseJson(String prefix, JsonNode node) {
        if (node.isObject()) { // 현재 노드가 JSON 오브젝트일 경우
            Iterator<String> fieldNames = node.fieldNames();
            while (fieldNames.hasNext()) {
                String fieldName = fieldNames.next();
                JsonNode childNode = node.get(fieldName);

                if(fieldName.equals("key")){//현재 오브젝트에서 필드명이 key일경우 key와 value를 한줄로 표시
                    fieldName = childNode.asText();
                    JsonNode tempChildNode = node.get(fieldNames.next());
                    Iterator<String> tempChildNodeName = tempChildNode.fieldNames();
                    System.out.println(prefix +"-"+fieldName+ " : " + tempChildNode.get(tempChildNodeName.next()));
                }else{
                    parseJson(prefix.isEmpty() ? fieldName : prefix + "-" + fieldName, childNode);
                }

            }
        } else if (node.isArray()) { // 현재 노드가 JSON 배열일 경우
            int index = 0;
            for (JsonNode arrayElement : node) {
                parseJson(prefix , arrayElement);
                index++;
            }
        } else { // 현재 노드가 값일 경우
            System.out.println(prefix + " : " + node.asText());
        }
    }
}
