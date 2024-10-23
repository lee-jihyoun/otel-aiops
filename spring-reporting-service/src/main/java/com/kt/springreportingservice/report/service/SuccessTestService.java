package com.kt.springreportingservice.report.service;


import com.kt.springreportingservice.report.domain.ErrorReport;
import com.kt.springreportingservice.report.repository.ErrorReportRepository;
import lombok.AllArgsConstructor;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Service;

import java.util.List;

@AllArgsConstructor
@Service
public class SuccessTestService {
    private final Logger logger = LoggerFactory.getLogger(getClass());

    ErrorReportRepository errorReportRepository;


    public void successTestService01() {
        String[] strings = {"1", "2", "3"};
        try {
            for (int i = 0; i <= strings.length; i++) {
                System.out.println(strings[i]);
            }
        } catch (Exception e) {
            logger.info("error " , e);  //2안
        }
    }

    public void successTestService02() {
        List<ErrorReport> errorReports = errorReportRepository.findAll();

        try {
            for (int i = 0; i <= errorReports.size(); i++) {
                System.out.println(errorReports.get(i));
            }
        } catch (Exception e) {
            logger.error("error " , e);  //2안
        }
    }

    public void successTestService03() {
        try {
            String nullString = null;
            System.out.println(nullString.length());
        } catch (Exception e) {
        }
    }

    public void successTestService04() {
//        String nullString = null;
//        System.out.println(nullString.length());
        logger.error("successTestService04 get data exception");
    }

    public void successTestService05() {
        Object obj = new String("test");
        Integer num = (Integer) obj;
    }

    public void successTestService06() {
    }

    public void successTestService07() {
        logger.error("successTestService07 get data parsing exception ");
    }

    public void successTestService08() {
        logger.info("successTestService08 call rest api exception ");
    }

    public void getErrorReport(){
        logger.info("get error report");
        List<ErrorReport>  errorReports= errorReportRepository.findAll();
        errorReports.get(0).setErrorReportSendYn("YYYYYYYYYYYYYYYYYYYYYYYY");
        errorReportRepository.save(errorReports.get(0));
    }
}
