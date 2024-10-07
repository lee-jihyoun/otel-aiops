package com.kt.springreportingservice.report.controller;


import com.kt.springreportingservice.report.domain.UserInfo;
import com.kt.springreportingservice.report.repository.UserInfoRepository;
import com.kt.springreportingservice.report.service.ErrorReportService;
import com.kt.springreportingservice.report.service.MailService;
import lombok.AllArgsConstructor;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;


@AllArgsConstructor
@RestController
public class ErrorReportController {

    private final Logger logger = LoggerFactory.getLogger(getClass());

    private UserInfoRepository userInfoRepository;



    @GetMapping("/")
    public void test() {
        List<UserInfo> userInfos = userInfoRepository.findAll();
        for(UserInfo userInfo : userInfos) {
            System.out.println(userInfo.getEmail());
        }
    }

}
