package com.kt.board.controller;



import com.kt.board.domain.LogApi;
import com.kt.board.service.LogService;
import lombok.RequiredArgsConstructor;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;

@RestController
@RequiredArgsConstructor
@RequestMapping("/log")
public class LogController {

    private final LogService logService;
    private static final Logger logger = LogManager.getLogger(LogController.class.getName());

    @GetMapping("/save")
    public void save(){

        LogApi logApi = logService.save();
        logger.info("### save in ### {}",logApi.toString());
        logger.warn("### save in ### {}",logApi.toString());
        try {
            Thread.sleep(5000);
        }catch (Exception e){
            e.printStackTrace();
        }
        logService.update(logApi);
        logger.info("### save out ### {}",logApi.toString());
    }

    @GetMapping("")
    public List<LogApi> logApiList(){
        logger.info("### info save in ### logApiList");
        logger.warn("### warn save in ### logApiList");
        logger.info("### info save out ### logApiList");
        return logService.all();
    }
}
