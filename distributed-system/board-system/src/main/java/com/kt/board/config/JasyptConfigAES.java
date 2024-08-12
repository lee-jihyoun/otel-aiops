package com.kt.board.config;

import com.ulisesbocchio.jasyptspringboot.annotation.EnableEncryptableProperties;
import org.jasypt.encryption.StringEncryptor;
import org.jasypt.encryption.pbe.PooledPBEStringEncryptor;
import org.jasypt.encryption.pbe.config.SimpleStringPBEConfig;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

import java.io.BufferedReader;
import java.io.FileReader;

@Configuration
@EnableEncryptableProperties
public class JasyptConfigAES {

    @Value("${encrypt.key-file.path}")
    private String keyFilePath;

    @Bean("jasyptEncryptorAES")
    public StringEncryptor jasyptEncryptorAES() {
        String key = "kim-sung-chul-project-properties-encrypt";
        PooledPBEStringEncryptor encryptor = new PooledPBEStringEncryptor();
        SimpleStringPBEConfig config = new SimpleStringPBEConfig();
//        config.setPassword(getKey());
        config.setPassword(key);
        config.setAlgorithm("PBEWITHHMACSHA512ANDAES_256");
        config.setKeyObtentionIterations("1000");
        config.setPoolSize("1");
        config.setProviderName("SunJCE");
        config.setSaltGeneratorClassName("org.jasypt.salt.RandomSaltGenerator");
        config.setIvGeneratorClassName("org.jasypt.iv.RandomIvGenerator");
        config.setStringOutputType("base64");
        encryptor.setConfig(config);
        return encryptor;
    }

    private String getKey() {
        String key="";
        try {
            BufferedReader reader = new BufferedReader(new FileReader(keyFilePath));
            key = reader.readLine();
        }catch (Exception e){
            e.printStackTrace();
        }
        return key;
    }
}
