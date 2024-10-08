package com.kt.springreportingservice.report.controller;


import com.kt.springreportingservice.report.domain.ErrorReport;
import com.kt.springreportingservice.report.repository.ErrorReportRepository;
//import com.kt.springreportingservice.report.repository.ErrorTestRepository;
import com.kt.springreportingservice.report.service.ErrorTestService;
import lombok.AllArgsConstructor;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;


@AllArgsConstructor
@RestController
public class ErrorTestController {

    private final Logger logger = LoggerFactory.getLogger(getClass());


    ErrorTestService errorTestService;

    // 배열 생성 후 없는 인덱스 조회 , ArrayIndexOutOfBoundsException
    @GetMapping("/error/test01")
    public void errorControllerTest01() {
        errorTestService.errorTestService01();
    }

    //데이터 조회 후 없는 인덱스 조회 ,IndexOutOfBoundsException
    @GetMapping("/error/test02")
    public void errorControllerTest02() {
        errorTestService.errorTestService02();
    }

    //길이가 1인 컬럼에 긴 데이터 넣으려는 시도 , DataIntegrityViolationException
    @GetMapping("/error/test03")
    public void errorControllerTest03() {
        errorTestService.errorTestService03();
    }

    //null인 데이터의 길이를 구함, NullPointerException
    @GetMapping("/error/test04")
    public void errorControllerTest04() {
        errorTestService.errorTestService04();
    }

    //String 타입을 Integer 타입으로 캐스팅 시도, ClassCastException
    @GetMapping("/error/test05")
    public void errorControllerTest05() {
        errorTestService.errorTestService05();
    }


    @GetMapping("/error/test06")
    public ResponseEntity<String> errorControllerTest06() {
        errorTestService.errorTestService06();
        return new ResponseEntity<>("", HttpStatus.INTERNAL_SERVER_ERROR);
    }

    @GetMapping("/error/test07")
    public ResponseEntity<String> errorControllerTest07() {
        errorTestService.errorTestService07();
        return new ResponseEntity<>("", HttpStatus.OK);
    }

    @GetMapping("/error/test08")
    public ResponseEntity<String> errorControllerTest08() {
        errorTestService.errorTestService08();
        return new ResponseEntity<>("", HttpStatus.INTERNAL_SERVER_ERROR);
    }

}
