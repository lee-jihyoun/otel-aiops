package com.kt.springotellistener.util;

import org.springframework.stereotype.Component;

import java.io.FileWriter;
import java.io.IOException;


@Component
public class FileUtil {

    public void saveToFile(String fileName , String data) {
        data = replaceString(data);
        try (FileWriter writer = new FileWriter(fileName, true)) {
            writer.write(data + System.lineSeparator());
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    public void tracesSaveToFile(String data) {
        data = replaceString(data);
        try (FileWriter writer = new FileWriter("traces.json", true)) {
            writer.write(data + System.lineSeparator());
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    public void metricsSaveToFile(String data) {
        data = replaceString(data);
        try (FileWriter writer = new FileWriter("metrics.json", true)) {
            writer.write(data + System.lineSeparator());
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    public void logsSaveToFile(String data) {
        data = replaceString(data);
        try (FileWriter writer = new FileWriter("logs.json", true)) {
            writer.write(data + System.lineSeparator());
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    public String replaceString(String data){
        return data.replaceAll("[\\s\\n\\r]+", " ").trim();


    }
}