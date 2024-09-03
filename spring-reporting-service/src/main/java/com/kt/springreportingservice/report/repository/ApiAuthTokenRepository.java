package com.kt.springreportingservice.report.repository;


import com.kt.springreportingservice.report.domain.ApiAuthToken;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.Optional;

public interface ApiAuthTokenRepository extends JpaRepository<ApiAuthToken, String> {

    Optional<ApiAuthToken> findByApiServiceName(String apiServiceName);
}
