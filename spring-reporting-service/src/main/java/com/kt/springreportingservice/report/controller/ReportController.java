package com.kt.springreportingservice.report.controller;


import com.kt.springreportingservice.report.domain.UserInfo;
import com.kt.springreportingservice.report.repository.UserInfoRepository;
import lombok.AllArgsConstructor;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;


@AllArgsConstructor
@RestController
public class ReportController {

    UserInfoRepository userInfoRepository;

    @GetMapping("/")
    public void test() {
        List<UserInfo> userInfos = userInfoRepository.findAll();
        for(UserInfo userInfo : userInfos) {
            System.out.println(userInfo.getEmail());
        }
    }


}
