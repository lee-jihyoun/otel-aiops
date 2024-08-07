package com.kt.board.domain;


import jakarta.persistence.*;
import lombok.*;

import java.time.LocalDateTime;

@Getter @Setter
@ToString
@Entity
@Table(name = "log_api")
@NoArgsConstructor
@AllArgsConstructor
public class LogApi {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long seq;

    @Column(name = "user_ip", length = 15)
    private String userIp;

    @Column(name = "user_id", length = 60)
    private String userId;

    @Column(name = "start_time")
    private LocalDateTime startTime;

        @Column(name = "end_time")
    private LocalDateTime endTime;

    @Column(name = "call_url", length = 100)
    private String callUrl;

    @Column(name = "call_url_parameter", length = 300)
    private String callUrlParameter;

    @PrePersist
    protected void onCreate() {
        LocalDateTime now = LocalDateTime.now();
        if (this.startTime == null) {
            this.startTime = now;
        }
        if (this.endTime == null) {
            this.endTime = now;
        }
    }
}