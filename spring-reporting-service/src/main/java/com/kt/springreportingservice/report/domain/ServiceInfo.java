package com.kt.springreportingservice.report.domain;

import jakarta.persistence.*;
import lombok.Getter;
import lombok.Setter;

import java.util.List;


@Getter
@Setter
@Entity
@Table(name = "service_info")
public class ServiceInfo {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long seq;

    @Column(name = "service_code", nullable = false, unique = true)
    private String serviceCode;

    @Column(name = "service_name_eng")
    private String serviceNameEng;

    @Column(name = "service_name_kr")
    private String serviceNameKr;

    @Column(name = "service_desc")
    private String serviceDesc;

    @OneToMany(mappedBy = "serviceInfo", cascade = CascadeType.ALL, fetch = FetchType.LAZY)
    private List<ErrorReport> errorReports;

    @OneToMany(mappedBy = "serviceInfo", cascade = CascadeType.ALL, fetch = FetchType.LAZY)
    private List<UserInfo> userInfos;

    // Getters and Setters
}

