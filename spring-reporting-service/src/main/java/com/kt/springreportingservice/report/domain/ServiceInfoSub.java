package com.kt.springreportingservice.report.domain;

import jakarta.persistence.*;
import lombok.Getter;
import lombok.Setter;
import org.hibernate.annotations.CreationTimestamp;

import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.List;


@Setter
@Getter
@Entity
@Table(name = "service_info_sub")
public class ServiceInfoSub {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long seq;

    @Column(name = "service_code_sub", length = 50)
    private String serviceCodeSub;

    @Column(name = "service_name_eng_sub", length = 100)
    private String serviceNameEngSub;

    @Column(name = "service_name_kr_sub", length = 100)
    private String serviceNameKrSub;

    @Column(name = "service_desc_sub", length = 5000)
    private String serviceDescSub;

    @CreationTimestamp
    @Column(name = "create_time", nullable = false, updatable = false)
    private LocalDateTime createTime;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "service_code", referencedColumnName = "service_code")
    private ServiceInfo serviceInfo;

    @OneToMany(mappedBy = "serviceInfoSub", cascade = CascadeType.ALL, orphanRemoval = true)
    private List<ErrorReport> errorReports = new ArrayList<>();
}
