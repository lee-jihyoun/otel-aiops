package com.kt.springreportingservice.report.repository;

import com.kt.springreportingservice.report.domain.ServiceInfo;
import com.kt.springreportingservice.report.domain.UserInfo;
import org.springframework.data.jpa.repository.JpaRepository;
import java.util.List;

public interface UserInfoRepository extends JpaRepository<UserInfo, Long> {
    List<UserInfo> findByServiceInfo(ServiceInfo serviceInfo);
}

