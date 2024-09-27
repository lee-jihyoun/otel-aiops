package com.kt.springotellistener.service;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.kt.springotellistener.util.DataUtil;
import lombok.AllArgsConstructor;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.redis.core.RedisTemplate;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Map;


@AllArgsConstructor
@Service
public class RedisService {


    private RedisTemplate<String, Object> redisTemplate;

    DataUtil dataUtil;

    public void saveToRedis(String hashKey, List<Map<String,Object>> dataList){
        hashKey += dataList.get(0).get("traceId").toString();
        for(Map<String,Object> map : dataList){
            String data = dataUtil.convertMapToJson(map);
            redisTemplate.opsForList().rightPush(hashKey,data);
        }

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
    public List<Object> getData(String id) {
        String redisKey = "key_hash:" + id;
        return redisTemplate.opsForList().range(redisKey, 0, -1); // 리스트 전체를 조회
    }
}