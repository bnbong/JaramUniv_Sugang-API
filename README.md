# JaramUniv_Sugang-API
자람 허브 스터디 최종 과제 - 수강 신청 API

@Author bnbong(이준혁, bbbong9@gmail.com)
   
## Directory Tree

### Entire Project
```
├── app
│   ├── v1 (FastAPI application)
│   │   ├── source files ...
│   │   ├── .gitignore
│   │   └── Dockerfile
│   └── v2 (Spring Boot application)
│       ├── source files ...
│       ├── .gitignore
│       └── Dockerfile
├── nginx (gateway)
│   └── conf
│   │   └── nginx.conf
│   └── logs
│       ├── access.log
│       └── error.log (contains warning)
├── .gitignore
├── docker-compose.yml
└── README.md
```

### v1 (FastAPI Application)
```
├── v1
│   └──  src
│   │   ├── controller
│   │   ├── db
│   │   ├── routers
│   │   ├── __init__.py
│   │   ├── context.py
│   │   └── settings.py
│   └──  tests
│       ├── __init__.py
│       ├── conftext.py
│       └──  test_initializer.py
├── .gitignore
├── Dockerfile
├── requirements.txt
├── setup.cfg
├── setup.py
└── main.py
```

### v2 (SpringBoot Application)
```
├── v2
│   ├──  .gradle
│   ├──  bin
│   ├──  build
│   ├──  gradle
│   └──  src
│       ├── main
│       │   └── java
│       │   │   └── com/jaramhub/sugangapi
│       │   │       └── SugangapiApplication.java
│       │   └── resources
│       │       ├── static
│       │       ├── templates
│       │       └── application.properties
│       └── test
│           └── java
│               └── com/jaramhub/sugangapi
│                   └── SugangapiApplicationTests.java
├── .gitignore
├── Dockerfile
├── HELP.md
├── build.gradle
├── gradlew
├── gradlew.bat
└── settings.gradle
```
버저닝을 붙여가며 다른 언어의 프레임워크로 두개의 버전을 사용하는 API를 작성한 이유는 FastAPI로 먼저 개발한 후 스터디에서 학습중인 Spring Boot를 사용하여 완전히 동일한 기능을 수행하는 API를 재작성해보고 싶어서 위와 같이 구성했습니다.

## API Documentation
### v1(FastAPI) Docs
 - will be added later

### v2(Spring Boot) Docs
 - will be added later

## Environments
### Development Env
 - Python 3.10.10 & FastAPI
 - Java OpenJDK 11 & Spring Boot 2.7.11
 - MariaDB

### Server Env
 - Ubuntu 20.04.5 LTS
 - Nginx
 - Docker

### Issue Managing Env
 - Github projects template Link
 - Jenkins (not sure ...)
 
## Deployments
 - will be added later

## Application Start Up
1. build SpringBoot Application to executable (at directory v2,): `./gradlew build`
2. Open CMD, and write command (at directory root,): `docker-compose up`

## DB & Module Information
 - Github wiki page link [here](https://github.com/bnbong/JaramUniv_Sugang-API/wiki)
 - access mariadb container : write command `docker exec -it jaramuniv_sugang-api-database-1 /bin/bash` & `mysql -u root -p`
 - check DB : `user jhubsugang`