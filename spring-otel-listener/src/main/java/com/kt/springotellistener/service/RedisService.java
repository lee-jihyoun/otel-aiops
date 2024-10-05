package com.kt.springotellistener.service;

import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.kt.springotellistener.util.DataUtil;
import lombok.AllArgsConstructor;
import org.springframework.data.redis.core.RedisTemplate;
import org.springframework.stereotype.Service;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.concurrent.TimeUnit;


@AllArgsConstructor
@Service
public class RedisService {


    private RedisTemplate<String, Object> redisTemplate;

    DataUtil dataUtil;

    public void saveToRedis(String type, List<Map<String,Object>> dataList){
        if(dataList.isEmpty()){
            return;
        }
        for(Map<String,Object> map : dataList){
            String key =map.get("traceId").toString();
            String listKey = getKey(type) +":"+key;

            String data = dataUtil.convertMapToJson(map);

            redisTemplate.opsForList().rightPush(listKey,data);
            redisTemplate.expire(listKey, 900, TimeUnit.SECONDS);
            if(type.equals("filtered_trace") || type.equals("filtered_log")){

                redisTemplate.opsForSet().add("key_store", key);
//                redisTemplate.opsForList().rightPush("key_store",key);
//                redisTemplate.opsForHash().put(key_store_key, "retry" , "0");
            }
        }
        //만료 시간 설정
//        redisTemplate.expire(key_store_key, 900, TimeUnit.SECONDS);

    }


    public void saveToRedisHash(String type, List<Map<String,Object>> dataList){
        if(dataList.isEmpty()){
            return;
        }
        for(Map<String,Object> map : dataList){
            String key =map.get("traceId").toString();
            String hashKey = getKey(type) +":"+key;
            String key_store_key = "key_store:"+key;
            String data = dataUtil.convertMapToJson(map);
            
            //여기서부터는 hash저장 
            String dataName = "";
            if(type.contains("trace")){
                dataName = "parsing_data_log";
            }else{
                dataName = "parsing_data_trace";
            }
            
            Object hash = redisTemplate.opsForHash().get(hashKey,dataName);
            if(hash !=null){
                try{
                    ObjectMapper objectMapper = new ObjectMapper();
                    List<Map<String, Object>> originData = objectMapper.readValue(hash.toString(), new TypeReference<List<Map<String, Object>>>(){});
                    originData.add(map);
                    redisTemplate.opsForHash().put(hashKey, dataName , dataUtil.convertListToString(originData));
                }catch (Exception e){
                    e.printStackTrace();
                }
            }else{
                List<Map<String,Object>> tempMap = new ArrayList<Map<String,Object>>();
                tempMap.add(map);
                redisTemplate.opsForHash().put(hashKey, dataName , dataUtil.convertListToString(tempMap));
            }
            //hash 저장 종료
            
            //리스트로 저장, 한줄이면됨
            //redisTemplate.opsForList().rightPush(hashKey,data);
            redisTemplate.expire(hashKey, 900, TimeUnit.SECONDS);
            if(type.equals("filtered_trace") || type.equals("filtered_log")){
                redisTemplate.opsForHash().put(key_store_key, "retry" , "0");
            }
        }
        //만료 시간 설정
//        redisTemplate.expire(key_store_key, 900, TimeUnit.SECONDS);

    }


    public String getKey(String key){
        String hash_key="";
        switch (key) {
            case "filtered_trace":
                hash_key= "filtered_trace_list";
            break;
            case "filtered_log":
                hash_key= "filtered_log_list";
            break;
            case "original_trace":
                hash_key= "original_trace_list";
            break;
            case "original_log":
                hash_key= "original_log_list";
            break;
        }
        return hash_key;
    }



    // String 값을 저장 (set)
    public void setValue(String key, String value) {
        redisTemplate.opsForValue().set(key, value);
    }

    // String 값 가져오기 (get)
    public String getValue(String key) {
        return (String) redisTemplate.opsForValue().get(key);
    }

    // Hash 값 저장 (hset)
    public void hsetValue(String key, String hashKey, String value) {
        redisTemplate.opsForHash().put(key, hashKey, value);
    }

    // Hash 값 가져오기 (hget)
    public String hgetValue(String key, String hashKey) {
        return (String) redisTemplate.opsForHash().get(key, hashKey);
    }

    // 데이터를 저장하는 메서드
    public void saveData(String id, String data) {
        String redisKey = "key_hash:" + id;

        redisTemplate.opsForList().rightPush(redisKey, data);

        // 해당 키가 Redis에 존재하는지 확인
//        Boolean hasKey = redisTemplate.hasKey(redisKey);


//        if (Boolean.TRUE.equals(hasKey)) {
//            // 키가 존재할 경우, 데이터를 리스트에 추가 (rpush)
//            redisTemplate.opsForList().rightPush(redisKey, data);
//        } else {
//            // 키가 없을 경우, 새로운 해시를 생성하고 리스트로 데이터를 저장
//            redisTemplate.opsForList().rightPush(redisKey, data);
//        }
    }

    // 데이터 조회 메서드
    public List<Object> getListData(String key) {

        return redisTemplate.opsForList().range(key, 0, -1); // 리스트 전체를 조회
    }

    public Object getHashData(String key){
        Object hash = redisTemplate.opsForHash().get(key,"parsing_data_log");
        return hash;
    }
}