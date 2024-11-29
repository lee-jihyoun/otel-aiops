package com.kt.springreportingservice.report.controller;


import com.kt.springreportingservice.report.domain.ErrorReport;
import com.kt.springreportingservice.report.domain.ServiceInfo;
import com.kt.springreportingservice.report.domain.ServiceInfoSub;
import com.kt.springreportingservice.report.domain.UserInfo;
import com.kt.springreportingservice.report.dto.MailSendInfosDto;
import com.kt.springreportingservice.report.repository.ErrorReportRepository;
import com.kt.springreportingservice.report.repository.UserInfoRepository;
import com.kt.springreportingservice.report.service.MailService;
import lombok.AllArgsConstructor;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RestController;

import java.util.ArrayList;
import java.util.List;


@AllArgsConstructor
@RestController
public class ErrorReportController {

    private final Logger logger = LoggerFactory.getLogger(getClass());

    private UserInfoRepository userInfoRepository;

    private ErrorReportRepository errorReportRepository;

    private MailService mailService;




    @GetMapping("/")
    public void test() {
        List<UserInfo> userInfos = userInfoRepository.findAll();
        for(UserInfo userInfo : userInfos) {
            System.out.println(userInfo.getEmail());
        }
    }

    @GetMapping("/serviceCode/{seq}")
    public String serviceCode(@PathVariable Long seq) {
        ErrorReport e = errorReportRepository.findById(seq).get();
        String serviceName = e.getServiceInfo().getServiceNameKr();
        String servicenameSub =e.getServiceInfoSub().getServiceNameKrSub();
        System.out.println(serviceName);
        System.out.println(servicenameSub);

        return "단위서비스명 : " + serviceName + "\n 하위 서비스명 : " + servicenameSub;
    }

    /*java.lang.OutOfMemoryError */
    @GetMapping("/getAllData")
    public List<ErrorReport> getData(){
        List<ErrorReport> errorReports = errorReportRepository.findAll();
        for (int i=0; i<1000000; i++) {
            List<ErrorReport> tempErrorReports = new ArrayList<>(errorReports);
            errorReports.addAll(tempErrorReports);
        }
        return errorReports;
    }

    /*java.net.ConnectException */
    @GetMapping("/getData")
    public List<MailSendInfosDto> getDatabaseData(){
        List<MailSendInfosDto> mailSendInfos = mailService.getAll();
        return mailSendInfos;
    }

    /*org.postgresql.util.PSQLException */
    @GetMapping("/saveData")
    public void saveData(){
        List<UserInfo> userInfos = userInfoRepository.findAll();
        for(UserInfo userInfo : userInfos) {
            userInfo.setEmail("kimsc1218@gmailaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa.com");
            userInfoRepository.save(userInfo);
        }

    }

}

