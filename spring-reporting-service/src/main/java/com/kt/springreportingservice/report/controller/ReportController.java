package com.kt.springreportingservice.report.controller;


import com.kt.springreportingservice.report.domain.UserInfo;
import com.kt.springreportingservice.report.repository.UserInfoRepository;
import com.kt.springreportingservice.report.service.MailService;
import lombok.AllArgsConstructor;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;


@AllArgsConstructor
@RestController
public class ReportController {

    private UserInfoRepository userInfoRepository;

    private MailService mailService;

    @GetMapping("/")
    public void test() {
        List<UserInfo> userInfos = userInfoRepository.findAll();
        for(UserInfo userInfo : userInfos) {
            System.out.println(userInfo.getEmail());
        }
    }

    @GetMapping("/mail")
    public void mailSendTest(){
        mailService.sendEmail("kimsc1218@gmail.com","테스트발송","냉무");
    }


}
