package com.kt.springreportingservice.report.service;

import com.kt.springreportingservice.report.domain.ApiAuthToken;
import com.kt.springreportingservice.report.domain.MailSendInfo;
import com.kt.springreportingservice.report.dto.MailSendInfosDto;
import com.kt.springreportingservice.report.repository.ApiAuthTokenRepository;
import com.kt.springreportingservice.report.repository.MailSendInfoRepository;
import jakarta.annotation.PostConstruct;
import jakarta.mail.internet.MimeMessage;
import org.modelmapper.ModelMapper;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.mail.javamail.JavaMailSender;
import org.springframework.mail.javamail.JavaMailSenderImpl;
import org.springframework.mail.javamail.MimeMessageHelper;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Optional;
import java.util.Properties;
import java.util.stream.Collectors;


// 해당 클래스는 lombok으로 사용하면 안됨
// JavaMailSender는 기본적으로 application-local.yml 파일을 읽어서 세팅을하는데
// 그러면 토큰값이 노출되서 DB로 바꿨음
// @AllArgsConstructor 를 사용하면 모든 필드에 자동으로 생성해줄려고 해서 오류발생함
// init 메서드를 별도로 만들어서 사용하려고 하다보니 아래와같이 @Autowired 을 사용해서 주입해서 써야함

@Service
public class MailService {

    private final Logger logger = LoggerFactory.getLogger(getClass());

    @Autowired
    private ApiAuthTokenRepository apiAuthTokenRepository;

    @Autowired
    ModelMapper modelMapper;


    private String gmailUserName;
    private String gmailAppToken;
    private JavaMailSender mailSender;
    @Autowired
    private MailSendInfoRepository mailSendInfoRepository;

    @PostConstruct
    public void init() {
        // DB에서 Gmail 토큰을 불러옴
        Optional<ApiAuthToken> tokenOpt = apiAuthTokenRepository.findByApiServiceName("gmail");
        if (tokenOpt.isPresent()) {
            ApiAuthToken token = tokenOpt.get();
            this.gmailUserName = token.getApiServiceId();
            this.gmailAppToken = token.getApiServiceToken();
            this.mailSender = createJavaMailSender(gmailUserName, gmailAppToken);
        } else {
            throw new IllegalStateException("Gmail token not found in the database");
        }
    }

    private JavaMailSender createJavaMailSender(String gmailUserName, String gmailAppToken) {
        JavaMailSenderImpl mailSender = new JavaMailSenderImpl();
        mailSender.setHost("smtp.gmail.com");
        mailSender.setPort(587);
        mailSender.setUsername(gmailUserName);
        mailSender.setPassword(gmailAppToken);

        Properties props = mailSender.getJavaMailProperties();
        props.put("mail.transport.protocol", "smtp");
        props.put("mail.smtp.auth", "true");
        props.put("mail.smtp.starttls.enable", "true");
        props.put("mail.debug", "false"); //SMTP 발송 로그

        return mailSender;
    }

    public void sendEmail(String to, String subject, String text) {

        MimeMessage message = mailSender.createMimeMessage();
        MimeMessageHelper helper=null;
        try{
            helper = new MimeMessageHelper(message, true, "UTF-8");
        }catch (Exception e){
            e.printStackTrace();
        }
        try{
            helper.setFrom(gmailUserName); //발신자 설정
            helper.setTo(to); // 수신자 설정
            helper.setSubject(subject); // 이메일 제목 설정
            helper.setText(text, true); // 본문 설정 (true: HTML 형식 사용)
        }catch (Exception e){
            logger.error(e.getMessage());
            e.printStackTrace();
        }
        mailSender.send(message); // 이메일 전송
        logger.info("### mail send end, to : {} , subject : {} , text : {} ", to, subject, text);
    }



//    public String formatContent(String content) {
//        // 정규식: 숫자+점(예: 1. 2. 3.) 뒤에 줄바꿈을 추가
//        return content.replaceAll("(\\d+\\. )", "\n\n$1");
//    }
//
//
//    public Map<String,String> createMailForm(ErrorReport errorReport)  {
//        /*
//        오류명 : error_name
//        오류 내용 :  error_content
//        오류 발생 시간 : created_time
//        오류 발생 위치 : error_location
//        오류 근본 원인 : error_cause
//        오류 해결 방법 : error_solution
//        */
//        Map<String,String> mailForm = new HashMap<>();
//        String mailContent="";
//        try{
//            ClassPathResource resource = new ClassPathResource("templates/error_report_mail_template.html.backup");
//            // 파일 내용을 읽음
//            mailContent = new String(Files.readAllBytes(Paths.get(resource.getURI())), StandardCharsets.UTF_8);
//        }catch (Exception e){
//            e.printStackTrace();
//        }
//
//        String mailTitle ="오류 리포트";
//        ServiceInfo serviceInfo = errorReport.getServiceInfo();
//        String errorCause = formatContent(errorReport.getErrorCause());
//        String errorSolution = formatContent(errorReport.getErrorSolution());
//        mailContent = mailContent.replace("{{service_name_en}}", serviceInfo.getServiceNameEng());
//        mailContent = mailContent.replace("{{service_name_kr}}", serviceInfo.getServiceNameKr());
//        mailContent = mailContent.replace("{{service_code}}", serviceInfo.getServiceCode());
//        mailContent = mailContent.replace("{{service_desc}}", serviceInfo.getServiceDesc());
//
//
//        mailContent = mailContent.replace("{{error_name}}", errorReport.getErrorName());
//        mailContent = mailContent.replace("{{created_time}}", errorReport.getCreateTime().toString());
//        mailContent = mailContent.replace("{{error_content}}", errorReport.getErrorContent());
//
//        mailContent = mailContent.replace("{{error_location}}", errorReport.getErrorLocation());
//        mailContent = mailContent.replace("{{error_cause}}", errorCause);
//        mailContent = mailContent.replace("{{service_impact}}", errorReport.getServiceImpact());
//
//        mailContent = mailContent.replace("{{error_solution}}", errorSolution);
//
//
//        mailForm.put("mailTitle" , mailTitle);
//        mailForm.put("mailContent" , mailContent);
//        return mailForm;
//    }

    public List<MailSendInfosDto> getAll(){
        List<MailSendInfo> mailSendInfos = mailSendInfoRepository.findAll();
        return mailSendInfos.stream()
                .map(this::convertToDTO)
                .collect(Collectors.toList());
    }

    public MailSendInfosDto convertToDTO(MailSendInfo mailSendInfo){
        MailSendInfosDto mailSendInfosDto = modelMapper.map(mailSendInfo, MailSendInfosDto.class);
        return mailSendInfosDto;
    }

}

