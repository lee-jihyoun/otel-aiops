package com.kt.springreportingservice.report.domain;

import jakarta.persistence.*;
import lombok.Getter;
import lombok.Setter;

import java.time.LocalDateTime;
import java.util.List;


@Getter
@Setter
@Entity
@Table(name = "error_report")
public class ErrorReport {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long seq;

    @ManyToOne
    @JoinColumn(name = "service_code", referencedColumnName = "service_code")
    private ServiceInfo serviceInfo;

    @Column(name = "error_name")
    private String errorName;

    @Column(name = "error_content", length = 5000)
    private String errorContent;

    @Column(name = "created_time")
    private LocalDateTime createdTime;

    @Column(name = "error_location", length = 500)
    private String errorLocation;

    @Column(name = "error_cause", length = 5000)
    private String errorCause;

    @Column(name = "error_solution", length = 5000)
    private String errorSolution;

    @OneToMany(mappedBy = "errorReport", cascade = CascadeType.ALL, fetch = FetchType.LAZY)
    private List<MailSendInfo> mailSendInfos;

    @Column(name = "error_report_send_yn", length = 1)
    private String errorReportSendYn;

    // Getters and Setters
}
