package com.kt.springreportingservice.report.domain;


import jakarta.persistence.*;
import lombok.Getter;
import lombok.Setter;

import java.time.LocalDateTime;

@Getter
@Setter
@Entity
@Table(name = "error_history")
public class ErrorHistory {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long seq;

    @ManyToOne
    @JoinColumn(name = "service_code", referencedColumnName = "service_code")
    private ServiceInfo serviceInfo;

    @Column(name = "exception_stacktrace", length = 500)
    private String exceptionStacktrace;

    @Column(name = "create_time")
    private LocalDateTime createTime;
}
