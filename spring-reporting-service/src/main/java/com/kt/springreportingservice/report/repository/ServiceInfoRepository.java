package com.kt.springreportingservice.report.repository;

import com.kt.springreportingservice.report.domain.ServiceInfo;
import org.springframework.data.jpa.repository.JpaRepository;

public interface ServiceInfoRepository extends JpaRepository<ServiceInfo, Long> {

}
