package com.kt.springreportingservice.report.controller;


//import com.kt.springreportingservice.report.repository.ErrorTestRepository;
import com.kt.springreportingservice.report.service.SuccessTestService;
import lombok.AllArgsConstructor;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;


@AllArgsConstructor
@RestController
public class SuccessTestController {

    private final Logger logger = LoggerFactory.getLogger(getClass());


    SuccessTestService successTestService;

    // 배열 생성 후 없는 인덱스 조회 , ArrayIndexOutOfBoundsException
    @GetMapping("/success/test01")
    public void errorControllerTest01() {
        successTestService.successTestService01();
    }

    //데이터 조회 후 없는 인덱스 조회 ,IndexOutOfBoundsException
    @GetMapping("/success/test02")
    public void errorControllerTest02() {
        successTestService.successTestService02();
    }

    //길이가 1인 컬럼에 긴 데이터 넣으려는 시도 , DataIntegrityViolationException
    @GetMapping("/success/test03")
    public void errorControllerTest03() {
        successTestService.successTestService03();
    }

    //null인 데이터의 길이를 구함, NullPointerException
    @GetMapping("/success/test04")
    public void errorControllerTest04() {
        successTestService.successTestService04();
    }

    //String 타입을 Integer 타입으로 캐스팅 시도, ClassCastException
    @GetMapping("/success/test05")
    public void errorControllerTest05() {
        successTestService.successTestService05();
    }


    @GetMapping("/success/test06")
    public ResponseEntity<String> errorControllerTest06() {
        successTestService.successTestService06();
        return new ResponseEntity<>("", HttpStatus.INTERNAL_SERVER_ERROR);
    }

    @GetMapping("/success/test07")
    public ResponseEntity<String> errorControllerTest07() {
        successTestService.successTestService07();
        return new ResponseEntity<>("", HttpStatus.OK);
    }

    @GetMapping("/success/test08")
    public ResponseEntity<String> errorControllerTest08() {
        successTestService.successTestService08();
        return new ResponseEntity<>("", HttpStatus.INTERNAL_SERVER_ERROR);
    }

    @GetMapping("/getErrorReport")
    public void getErrorReport() {
        logger.info("getErrorReport controller in");
        successTestService.getErrorReport();
    }

}
