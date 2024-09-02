package com.kt.springreportingservice.report.repository;

import com.kt.springreportingservice.report.domain.MailSendInfo;
import org.springframework.data.jpa.repository.JpaRepository;

public interface MailSendInfoRepository extends JpaRepository<MailSendInfo, Long> {

}
