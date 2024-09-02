package com.kt.springreportingservice.report.repository;

import com.kt.springreportingservice.report.domain.ErrorReport;
import org.springframework.data.jpa.repository.JpaRepository;
import java.util.List;

public interface ErrorReportRepository extends JpaRepository<ErrorReport, Long> {
    List<ErrorReport> findByErrorReportSendYn(String errorReportSendYn);
}

