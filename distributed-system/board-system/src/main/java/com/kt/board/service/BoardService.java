package com.kt.board.service;



import com.kt.board.domain.Board;
import com.kt.board.domain.LogApi;
import com.kt.board.repository.BoardRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.data.domain.PageRequest;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
@RequiredArgsConstructor
public class BoardService {

    private final BoardRepository boardRepository;
    private final LogService logService;

    public List<Board> all(){
        LogApi logApi = logService.save();
        List<Board> boardList = boardRepository.findAll();
        logService.update(logApi);
        return boardList;
    }


    //@WithSpan
    public List<Board> all(int pageSize){
        LogApi logApi = logService.save();
        PageRequest pageRequest = PageRequest.of(0, pageSize);
        List<Board> boardList = boardRepository.findAll(pageRequest).getContent();
        logService.update(logApi);

        return boardList;
    }
}
