# JaramUniv_Sugang-API
한양대학교 ERICA 소프트웨어융합대학 학회 자람 소속 스터디 **자람 허브** 최종 과제 프로젝트

@Author 자람 39기 이준혁(bnbong, bbbong9@gmail.com)

## 수강 신청 API 개발
### 0. 개요

자람 대학교에서는 수강 신청 API를 통해 개설 과목을 등록하고, 학생들이 해당 개설 과목에 수강 신청을 할 수 있게 하고자 한다.

### 1. 데이터 요구 사항

해당 API에서 아래와 같은 정보들을 DB를 통해 관리할 수 있어야 한다.

### a) 회원 정보

- 회원의 이메일
    - 한 이메일은 한 개의 계정에서만 사용 가능하다.
    - RFC 2821 표준에 따르면 이메일의 최대 길이는 256자라고 한다.
- 회원의 실명
    - 자람 대학교에서는 척화비가 있어 외국인이 없다고 가정한다.
    - 회원의 이름들은 10자를 넘지 않는다고 가정한다.
- 회원의 전공
    - 학생일 경우, 해당 학생의 전공, 교수일 경우 해당 교수의 담당 전공이다.
    - 현재 자람 대학교에는 아래 학과들이 존재한다.
        
        
        | 전공 분류코드 | 전공명 |
        | --- | --- |
        | SW100 | 소프트웨어학과 |
        | AI222 | 인공지능학과 |
        | ICT12 | ICT 융합학과 |
        | PYS12 | 물리학과 |
        | MATH1 | 수학과 |
        | DUKNW | 구근모를아십니과 |
        | TP100 | 내거친생각과 |
        | DLA73 | 불안한눈빛과 |
        | ABCDE | 그걸지켜보는과 |
    - **자람 대학교에서는 학과가 자주 변경되는 것으로 보인다. 최근 1개의 학과의 명칭이 변경되었으며, 1개의 새로운 과가 추가되었다.**
- 회원 유형
    - 교수 회원인지, 학생 회원인지 구분할 수 있어야 한다.
    - 다른 회원 유형은 앞으로도 추가되지 않는다고 가정한다.

### b) 개설 과목

- 개설 과목 소속 학과
- 개설 과목 이름
    - 최대 30자를 넘지 않는다고 가정한다.
- 개설 과목 설명
    - 최대 255자 정도의 설명을 저장할 수 있어야 한다.
- 개설 과목 담당 교수
- 개설 과목 정원

### c) 수강 신청 정보

- 수강 신청을 한 회원
- 수강 신청을 한 과목
- 수강 신청을 한 시간("yyyy-mm-dd HH:MM:SS")

*그 외 필요한 정보는 마음껏 추가 가능하다.*

*해석을 쉽게 하기 위해 데이터를 3그룹으로 묶었을 뿐, 실제 테이블을 3개를 사용하라는 의미가 아니다.*

*모든 데이터는 무결성을 가져야 한다.*

### 2. 기능 요구 사항

모든 요청에 대하여, request header에 그 요청을 보낸 회원의 정보가 담겨 있다고 가정하고 개발한다.

user_pk : 요청을 보낸 회원의 pk

### a) 회원 정보

1. 단일 회원 조회
2. 단일 회원 추가
3. 단일 회원 삭제
4. 단일 회원 정보 수정
5. 학생 회원 전체를 불러오기
6. 교수 회원 전체를 불러오기

### b) 과목 개설

1. 단일 과목 조회
    - 수강 신청 인원이 함께 조회 되어야 한다.
2. 단일 과목 추가
3. 단일 과목 삭제
4. 단일 과목 정보 수정
5. 특정 학과 과목 불러오기

### c) 수강 신청

1. 단일 과목에 대하여 수강 신청
    - 해당 과목의 수강 신청 인원이 가득 찬 경우 수강 신청을 할 수 없다.
    - 교수 회원은 수강 신청을 할 수 없다.
2. 단일 과목에 대하여 수강 포기
    - 교수 회원은 이 기능을 사용할 수 없다.
3. 특정 회원의 수강 신청 정보 조회
4. 특정 과목을 수강 신청한 전체 회원 정보 조회
5. 과목 폐강
    - 과목에 대한 수강 신청 기록이 전부 삭제되어야 한다.(CASCADE 금지)

이 제약 조건에 따르면, 과목에 대한 수강 신청 기록이 전부 삭제되어야 하는 상황에서 CASCADE를 사용하면 안됩니다. CASCADE는 관계형 데이터베이스에서 부모 테이블의 레코드가 삭제될 때 자식 테이블의 관련 레코드도 자동으로 삭제하는 옵션입니다.

주의해야 할 점은 다음과 같습니다:

데이터베이스 스키마: 과목과 수강 신청 간의 관계를 나타내는 외래 키(Foreign Key) 설정 시, CASCADE 옵션을 사용하지 않아야 합니다. 대신, 수강 신청 레코드를 삭제하는 것이 필요한 경우 명시적으로 해당 레코드를 먼저 삭제해야 합니다.

CRUD 메소드 작성: 과목을 삭제하기 전에 관련 수강 신청 레코드를 모두 삭제하는 메소드를 작성하고, 이를 호출해야 합니다. 과목 삭제 시 자동으로 관련 수강 신청 레코드가 삭제되지 않으므로 이러한 절차가 필요합니다.

예를 들어, DELETE 요청이 과목을 삭제하기 전에 먼저 해당 과목에 대한 모든 수강 신청 기록을 삭제해야 합니다. 이를 위해 다음과 같은 순서로 작업을 수행할 수 있습니다:

1. 해당 과목에 대한 모든 수강 신청 레코드를 검색합니다.
2. 검색된 수강 신청 레코드를 반복하면서 각 레코드를 삭제합니다.
3. 모든 수강 신청 레코드가 삭제된 후, 과목 레코드를 삭제합니다.

이렇게 하면 CASCADE를 사용하지 않고도 과목 삭제 시 관련 수강 신청 기록을 전부 삭제할 수 있습니다. 이러한 제약 조건을 충족시키기 위해 명시적으로 수강 신청 레코드 삭제와 과목 삭제를 구현해야 합니다.

*상세한 제약 요건이 없는 기능은 요령 것 구현하라*

*request body와 response body는 자율적으로 결정한다. 하지만, 이때 왜 그런 식으로 body를 결정하였는지,사유가 필요하다.*

*어떤 Path로  API를 구성하지도 자율적으로 결정한다. 하지만, 마찬가지로 그렇게 path를 설계한 사유가 필요하다.*

*해당 API에 대한 문서화를 진행한다. 어떤 툴을 사용하던 상관 없다.*

### 3. 기타 제약 요건

- DBMS는 Mariadb 하나로 제한한다.
- 사용 가능한 프레임 워크는 현재 학습중인 프레임워크를 사용하도록 한다.

---
   
## Directory Tree

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
├── docker-compose.prod.yml
├── docker-compose.yml
└── README.md
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
 - Docker & Docker-compose

### Server Env
 - Oracle Cloud Computing Instance (ARM-based Ampere A1 Compute)
 - Ubuntu 20.04 LTS
 - Nginx

### CI/CD
 - Jenkins (CD)
 - Github Action (CI)

## Application Start Up
1. build SpringBoot Application to executable (at directory v2,): `./gradlew build`
2. Open CMD, and write command (at directory root,): `docker compose up -f docker-compose.yml -d`

## DB & Module Information
 - Github wiki page link [here](https://github.com/bnbong/JaramUniv_Sugang-API/wiki)
 - access mariadb container : write command `docker exec -it jaramuniv_sugang-api-database-1 bash` & `mysql -u jhubsugang -p{password}`