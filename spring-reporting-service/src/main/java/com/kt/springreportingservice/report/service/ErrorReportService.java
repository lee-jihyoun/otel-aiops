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
        //서비스 정보
        errorReportMap.put("service_name_en", errorReport.getServiceInfo().getServiceNameEng());
        errorReportMap.put("service_name_kr", errorReport.getServiceInfo().getServiceNameKr());
        errorReportMap.put("service_code", errorReport.getServiceInfo().getServiceCode());
        errorReportMap.put("service_desc", errorReport.getServiceInfo().getServiceDesc());

        //하위 서비스 정보
        Optional.ofNullable(errorReport.getServiceInfoSub()).ifPresent(serviceInfoSub -> {
            errorReportMap.put("service_name_en_sub", serviceInfoSub.getServiceNameEngSub());
            errorReportMap.put("service_name_kr_sub", serviceInfoSub.getServiceNameKrSub());
            errorReportMap.put("service_code_sub", serviceInfoSub.getServiceCodeSub());
            errorReportMap.put("service_desc_sub", serviceInfoSub.getServiceDescSub());
        });

        //오류 정보
        errorReportMap.put("error_name", errorReport.getErrorName());
        errorReportMap.put("error_created_time", errorReport.getErrorCreateTime());
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
        // 1번은 제외, 2번 이상 숫자 앞에 줄바꿈 2번 추가
        content = content.replaceAll("(?<!\\d)([2-9]\\d*\\. )", "\n\n\n$1");
        // : - 또는 . - 패턴일 때 - 앞에 줄바꿈 추가
        content = content.replaceAll("([.:]\\s?)(-)", "$1\n\n$2");
        return content;
    }

}
