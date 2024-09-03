package com.kt.springreportingservice.report.service;

import com.kt.springreportingservice.report.domain.ApiAuthToken;
import com.kt.springreportingservice.report.repository.ApiAuthTokenRepository;
import jakarta.annotation.PostConstruct;
import lombok.AllArgsConstructor;
import lombok.NoArgsConstructor;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.mail.SimpleMailMessage;
import org.springframework.mail.javamail.JavaMailSender;
import org.springframework.mail.javamail.JavaMailSenderImpl;
import org.springframework.stereotype.Service;

import java.util.Optional;
import java.util.Properties;


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


    private String gmailUserName;
    private String gmailAppToken;
    private JavaMailSender mailSender;

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
        logger.info("### mail send start");
        SimpleMailMessage message = new SimpleMailMessage();
        message.setFrom(gmailUserName);
        message.setTo(to);
        message.setSubject(subject);
        message.setText(text);
        mailSender.send(message);
        logger.info("### mail send end, to : {} , subject : {} , text : {} ", to, subject, text);
    }
}

