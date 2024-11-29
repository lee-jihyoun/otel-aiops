package com.kt.springreportingservice.report.domain;


import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.Id;
import jakarta.persistence.Table;
import lombok.Getter;
import lombok.Setter;

@Setter
@Getter
@Entity
@Table(name = "error_test_domain")
public class ErrorTestDomain {

    @Id
    @Column(name = "error_domain", length = 50, nullable = false)
    private String errorDomain;

    @Column(name = "error_test", length = 50)
    private String errorTest;
}
