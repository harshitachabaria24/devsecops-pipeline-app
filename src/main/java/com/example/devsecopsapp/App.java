package com.example.devsecopsapp;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

import software.amazon.awssdk.regions.Region;
import software.amazon.awssdk.services.s3.S3Client;
import software.amazon.awssdk.services.s3.model.*;
import software.amazon.awssdk.core.sync.RequestBody;
import software.amazon.awssdk.core.ResponseInputStream;
import software.amazon.awssdk.services.s3.model.GetObjectResponse;

import java.io.IOException;
import java.util.UUID;

@SpringBootApplication
@RestController
public class App {

    private final S3Client s3 = S3Client.builder().region(Region.US_EAST_1).build();
    private final String bucket = System.getenv("BUCKET_NAME");

    public static void main(String[] args) {
        SpringApplication.run(App.class, args);
    }

    @GetMapping("/health")
    public ResponseEntity<String> health() {
        return ResponseEntity.ok("OK");
    }

    @PostMapping("/upload")
    public String uploadFile(@RequestParam("file") MultipartFile file) throws IOException {
        String key = UUID.randomUUID().toString() + "-" + file.getOriginalFilename();
        PutObjectRequest req = PutObjectRequest.builder()
                .bucket(bucket)
                .key(key)
                .serverSideEncryption(ServerSideEncryption.AWS_KMS)
                .build();
        s3.putObject(req, RequestBody.fromBytes(file.getBytes()));
        return key;
    }

    @GetMapping("/download")
    public ResponseEntity<byte[]> downloadFile(@RequestParam("key") String key) throws IOException {
        GetObjectRequest req = GetObjectRequest.builder().bucket(bucket).key(key).build();
        ResponseInputStream<GetObjectResponse> s = s3.getObject(req);
        byte[] bytes = s.readAllBytes();
        return ResponseEntity.ok().body(bytes);
    }
}
