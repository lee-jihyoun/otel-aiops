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
public class ErrorTestService {
    private final Logger logger = LoggerFactory.getLogger(getClass());

    ErrorReportRepository errorReportRepository;


    public void errorTestService01() {
        String[] strings = {"1", "2", "3"};
        try {
            for (int i = 0; i <= strings.length; i++) {
                System.out.println(strings[i]);
            }
        } catch (Exception e) {
            logger.info("###########/error/test01");
        }
    }

    public void errorTestService02() {
        List<ErrorReport> errorReports = errorReportRepository.findAll();

        try {
            for (int i = 0; i <= errorReports.size(); i++) {
                System.out.println(errorReports.get(i));
            }
        } catch (Exception e) {
            logger.error("###########/error/test02");
        }
    }

    public void errorTestService03() {
        List<ErrorReport> errorReports = errorReportRepository.findAll();
        try {
            for (ErrorReport errorReport : errorReports) {
                errorReport.setErrorReportSendYn("YYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYY");
                errorReportRepository.save(errorReport);
            }
        } catch (Exception e) {
        }
    }

    public void errorTestService04() {
//        String nullString = null;
//        System.out.println(nullString.length());
        logger.error("###########/error/test04");
    }

    public void errorTestService05() {
        Object obj = new String("test");
        Integer num = (Integer) obj;
    }

    public void errorTestService06() {
    }

    public void errorTestService07() {
        logger.error("###########/error/test07");
    }

    public void errorTestService08() {
        logger.info("###########/error/test08");
    }
}
