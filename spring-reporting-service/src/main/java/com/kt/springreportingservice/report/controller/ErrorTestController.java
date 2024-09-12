package com.kt.springreportingservice.report.controller;


import com.kt.springreportingservice.report.domain.ErrorReport;
import com.kt.springreportingservice.report.repository.ErrorReportRepository;
import com.kt.springreportingservice.report.repository.ErrorTestRepository;
import lombok.AllArgsConstructor;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;


@AllArgsConstructor
@RestController
public class ErrorTestController {

    ErrorTestRepository errorTestRepository;

    ErrorReportRepository errorReportRepository;

    //없는 데이터베이스 조회 , InvalidDataAccessResourceUsageException
    @GetMapping("/error/test01")
    public void errorTest01() {
        errorTestRepository.findAll();
    }

    // 배열 생성 후 없는 인덱스 조회 , ArrayIndexOutOfBoundsException
    @GetMapping("/error/test02")
    public void errorTest02() {

        String [] strings = {"1", "2", "3"};

        for(int i=0; i<=strings.length; i++) {
            System.out.println(strings[i]);
        }
    }

    //데이터 조회 후 없는 인덱스 조회 ,IndexOutOfBoundsException
    @GetMapping("/error/test03")
    public void errorTest03() {
        List<ErrorReport> errorReports = errorReportRepository.findAll();

        for (int i=0;i<=errorReports.size();i++) {
            System.out.println(errorReports.get(i));
        }
    }

    //길이가 1인 컬럼에 긴 데이터 넣으려는 시도 , DataIntegrityViolationException
    @GetMapping("/error/test04")
    public void errorTest04() {
        List<ErrorReport> errorReports = errorReportRepository.findAll();
        for(ErrorReport errorReport : errorReports) {
            errorReport.setErrorReportSendYn("YYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYY");
            errorReportRepository.save(errorReport);
        }
    }

    //null인 데이터의 길이를 구함, NullPointerException
    @GetMapping("/error/test05")
    public void errorTest05() {
        String nullString = null;
        System.out.println(nullString.length());
    }

    //String 타입을 Integer 타입으로 캐스팅 시도, ClassCastException
    @GetMapping("/error/test06")
    public void errorTest06() {
        Object obj = new String("test");
        Integer num = (Integer) obj;
    }

    //String타입을 Integer타입으로 변환 시도, NumberFormatException
    @GetMapping("/error/test07")
    public void errorTest07() {
        String invalidNumber = "abc";
        Integer.parseInt(invalidNumber);  
    }


}
