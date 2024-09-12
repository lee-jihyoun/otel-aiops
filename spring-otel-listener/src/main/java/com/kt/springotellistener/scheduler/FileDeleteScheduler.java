package com.kt.springotellistener.scheduler;


import lombok.AllArgsConstructor;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Component;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;

@AllArgsConstructor
@Component
public class FileDeleteScheduler {

    private final Logger logger = LoggerFactory.getLogger(getClass());

    @Scheduled(fixedRate = 3600000) // 1시간마다 실행
//    @Scheduled(fixedRate = 60000) // 1분마다 실행
    public void fileDelete() {
        String []fileNameList = {"original_logs.json" , "original_metrics.json" , "original_span.json"};
        for(String fileName : fileNameList) {
            try {
                Files.deleteIfExists(Paths.get(fileName));
                logger.info("### Deleted file: " + fileName);
            } catch (IOException e) {
                logger.error(e.getMessage());
                e.printStackTrace();
            }
        }

    }
}
