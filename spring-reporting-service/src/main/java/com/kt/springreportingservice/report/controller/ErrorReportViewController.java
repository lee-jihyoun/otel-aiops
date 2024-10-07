package com.kt.springreportingservice.report.controller;

import com.kt.springreportingservice.report.domain.ErrorReport;
import com.kt.springreportingservice.report.repository.ErrorReportRepository;
import com.kt.springreportingservice.report.service.ErrorReportService;
import com.kt.springreportingservice.report.service.MailService;
import lombok.AllArgsConstructor;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;

import java.util.Map;
import java.util.Optional;

@AllArgsConstructor
@Controller
public class ErrorReportViewController {
    private final Logger logger = LoggerFactory.getLogger(getClass());

    ErrorReportService errorReportService;



    @GetMapping("/report/{seq}")
    public String getErrorReport(@PathVariable Long seq, Model model) {

        ErrorReport errorReport = errorReportService.getErrorReport(seq);
        Map<String,Object>errorReportMap =  errorReportService.errorReportToMap(errorReport);
        model.addAllAttributes(errorReportMap);
        return "error_report_template";
    }


}
