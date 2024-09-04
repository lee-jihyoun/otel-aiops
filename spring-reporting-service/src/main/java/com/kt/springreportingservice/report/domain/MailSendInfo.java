package com.kt.springreportingservice.report.domain;

import jakarta.persistence.*;
import lombok.Getter;
import lombok.Setter;


@Getter
@Setter
@Entity
@Table(name = "mail_send_info")
public class MailSendInfo {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long seq;

    @ManyToOne
    @JoinColumn(name = "error_report_seq", nullable = false)
    private ErrorReport errorReport;

    @Column(name = "service_code")
    private String serviceCode;

    @Column(name = "is_mail_sent")
    private String isMailSent;

    @Column(name = "receiver_email")
    private String receiverEmail;

    // Getters and Setters
}