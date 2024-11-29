package com.kt.springreportingservice.report.dto;

import com.kt.springreportingservice.report.domain.ErrorReport;
import lombok.Getter;
import lombok.Setter;

import java.time.LocalDateTime;

@Getter
@Setter
public class MailSendInfosDto{
    private Long seq;
    private String serviceCode;
    private String isMailSent;
    private String receiverEmail;
    private LocalDateTime createTime;
}
