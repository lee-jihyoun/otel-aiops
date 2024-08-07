package com.kt.board.repository;



import com.kt.board.domain.LogApi;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;
import org.springframework.transaction.annotation.Transactional;


@Repository
@Transactional
public interface LogRepository extends JpaRepository<LogApi, Long> {

}
