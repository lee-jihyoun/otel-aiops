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

    @Column(name = "trace_exception_stacktrace_short", length = 500)
    private String traceExceptionStacktraceShort;

    @Column(name = "log_exception_stacktrace_short", length = 500)
    private String logExceptionStacktraceShort;

    @Column(name = "create_time")
    private LocalDateTime createTime;

    @Column(name ="cnt")
    private int cnt;
}
