package com.kt.board.service;



import com.kt.board.domain.LogApi;
import com.kt.board.repository.LogRepository;
import jakarta.servlet.http.HttpServletRequest;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.web.context.request.RequestContextHolder;
import org.springframework.web.context.request.ServletRequestAttributes;

import java.time.LocalDateTime;
import java.util.List;
import java.util.UUID;

@Service
@RequiredArgsConstructor
public class LogService {

    private final LogRepository logRepository;


    public LogApi save(){
        HttpServletRequest req = ((ServletRequestAttributes) RequestContextHolder.currentRequestAttributes()).getRequest();
        String ip = req.getHeader("x-forwarded-for");
        String httpMethod = req.getMethod();
        String httpUrl = req.getRequestURL().toString();
        String httpUri = req.getRequestURI();
        String queryString = req.getQueryString();
        String fullUrl = queryString == null ? httpUrl : httpUrl + "?" + queryString;
        String uuid = UUID.randomUUID().toString();

        LogApi logApi = new LogApi();
        logApi.setUserId(uuid);
        logApi.setUserIp(ip);
        logApi.setCallUrl(fullUrl);
        logApi.setCallUrlParameter(queryString);
        logRepository.save(logApi);
//        System.out.println("logApi seq : " + logApi);
        return logApi;
    }

    public void update(LogApi logApi){
//        System.out.println("## log update");
        LocalDateTime now = LocalDateTime.now();
        logApi.setEndTime(now);
        logRepository.save(logApi);
    }

    public List<LogApi> all(){
        return logRepository.findAll();
    }


}
