package com.kt.springreportingservice.report.domain;

import jakarta.persistence.*;
import lombok.Getter;
import lombok.Setter;

import java.time.LocalDateTime;


@Setter
@Getter
@Entity
@Table(name = "api_auth_tokens")
public class ApiAuthToken {

    @Id
    @Column(name = "api_service_name", length = 50, nullable = false)
    private String apiServiceName;

    @Column(name = "api_service_id", length = 50)
    private String apiServiceId;

    @Column(name = "api_service_token", length = 500)
    private String apiServiceToken;

    @Column(name = "create_time", nullable = false)
    private LocalDateTime createTime;

    @Column(name = "etc", length = 500)
    private String etc;


}

