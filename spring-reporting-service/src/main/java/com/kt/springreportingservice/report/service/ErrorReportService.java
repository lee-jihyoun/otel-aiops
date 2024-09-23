package com.kt.springreportingservice.report.service;


import com.kt.springreportingservice.report.domain.ErrorReport;
import com.kt.springreportingservice.report.repository.ErrorReportRepository;
import lombok.AllArgsConstructor;
import org.springframework.stereotype.Service;
import org.thymeleaf.context.Context;
import org.thymeleaf.spring6.SpringTemplateEngine;

import java.util.HashMap;
import java.util.Map;
import java.util.Optional;


@AllArgsConstructor
@Service
public class ErrorReportService {

    ErrorReportRepository errorReportRepository;

    private SpringTemplateEngine templateEngine;

    public ErrorReport getErrorReport(Long seq) {
        Optional<ErrorReport> optionalErrorReport = errorReportRepository.findById(seq);
        ErrorReport errorReport = optionalErrorReport.get();
        return errorReport;
    }

    //domain 클래스를 map 으로 변환
    public Map<String, Object> errorReportToMap(ErrorReport errorReport) {
        Map<String, Object> errorReportMap = new HashMap<>();
        String errorCause = formatContent(errorReport.getErrorCause());
        String errorSolution = formatContent(errorReport.getErrorSolution());
        errorReportMap.put("service_name_en", errorReport.getServiceInfo().getServiceNameEng());
        errorReportMap.put("service_name_kr", errorReport.getServiceInfo().getServiceNameKr());
        errorReportMap.put("service_code", errorReport.getServiceInfo().getServiceCode());
        errorReportMap.put("service_desc", errorReport.getServiceInfo().getServiceDesc());
        errorReportMap.put("error_name", errorReport.getErrorName());
        errorReportMap.put("created_time", errorReport.getCreateTime());
        errorReportMap.put("error_content", errorReport.getErrorContent());
        errorReportMap.put("error_location", errorReport.getErrorLocation());
        errorReportMap.put("service_impact", errorReport.getServiceImpact());
        errorReportMap.put("error_cause", errorCause);
        errorReportMap.put("error_solution", errorSolution);
        return errorReportMap;
    }

    
    //Thymeleaf 템플릿으로 메일 발송
    public String templateModel(ErrorReport errorReport) {
        Map<String, Object> templateModel = errorReportToMap(errorReport);
        // Thymeleaf 템플릿에서 사용할 컨텍스트 설정
        Context context = new Context();
        context.setVariables(templateModel);
        // HTML 템플릿 렌더링
        String htmlContent = templateEngine.process("error_report_template", context);
        return htmlContent;
    }

    public String formatContent(String content) {
        // 정규식: 숫자+점(예: 1. 2. 3.) 뒤에 줄바꿈을 추가
        return content.replaceAll("(\\d+\\. )", "\n\n$1");
    }

}
