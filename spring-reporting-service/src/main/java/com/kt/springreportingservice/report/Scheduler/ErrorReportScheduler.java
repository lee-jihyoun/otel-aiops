package com.kt.springreportingservice.report.Scheduler;

import com.kt.springreportingservice.report.domain.ErrorReport;
import com.kt.springreportingservice.report.domain.MailSendInfo;
import com.kt.springreportingservice.report.domain.ServiceInfo;
import com.kt.springreportingservice.report.domain.UserInfo;
import com.kt.springreportingservice.report.repository.ErrorReportRepository;
import com.kt.springreportingservice.report.repository.MailSendInfoRepository;
import com.kt.springreportingservice.report.repository.UserInfoRepository;
import com.kt.springreportingservice.report.service.MailService;
import lombok.AllArgsConstructor;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Component;
import org.springframework.transaction.annotation.Transactional;

import java.util.HashMap;
import java.util.List;
import java.util.Map;


@AllArgsConstructor
@Component
public class ErrorReportScheduler {

    private final Logger logger = LoggerFactory.getLogger(getClass());

    private ErrorReportRepository errorReportRepository;

    private UserInfoRepository userInfoRepository;

    private MailSendInfoRepository mailSendInfoRepository;

    private MailService mailService;

    @Transactional
    @Scheduled(fixedRate = 60000) // 1분마다 실행
    public void checkErrorReports() {




        logger.info("### ErrorReportScheduler started");
        List<ErrorReport> errorReports = errorReportRepository.findByErrorReportSendYn("N"); // 'N'인 데이터만 조회

        if (!errorReports.isEmpty()) {
            for (ErrorReport errorReport : errorReports) {
                ServiceInfo serviceInfo = errorReport.getServiceInfo(); // ServiceInfo 객체를 가져옴
                String serviceCode = serviceInfo.getServiceCode(); // ServiceInfo에서 serviceCode 가져옴

                // user_info 테이블에서 service_code로 사용자 목록 조회
                List<UserInfo> users = userInfoRepository.findByServiceInfo(serviceInfo);

                for (UserInfo user : users) {
                    //메일발송
                    mailService.sendEmail(user.getEmail(), errorReport.getErrorName(), errorReport.getErrorContent());
                    
                    MailSendInfo mailSendInfo = new MailSendInfo();
                    mailSendInfo.setReceiverEmail(user.getEmail());
                    mailSendInfo.setErrorReport(errorReport); // ErrorReport 객체를 직접 설정
                    mailSendInfo.setServiceCode(serviceCode); // serviceCode 설정
                    mailSendInfo.setIsMailSent("Y");
                    mailSendInfoRepository.save(mailSendInfo);
                }
                errorReport.setErrorReportSendYn("Y");
                errorReportRepository.save(errorReport);
            }
        }
        logger.info("### ErrorReportScheduler ended");
    }
}
