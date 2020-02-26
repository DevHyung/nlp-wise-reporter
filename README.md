# Wise-Reporter

Wise-Report 진행하면서 썼던 Module + Code 저장 repository

## 1.1 Directory hierarchy
```bash
├─Github
│  │  README.md
│  │  requirements.txt
│  │  .gitignore
│  │
│  ├─ DB
│  │      __init__.py       # init 
│  │      db_pull.py        # WiseReporter DB pull script 
│  │      requirements.txt  # DB 사용시 필요한 패키지  
│  │      CONFIG.py         # Private file (DB connection info)
│  │    
│  ├─ preprocessing
│  │      datas/            # {}.txt 로 각 회사별로 URL들이 저장되어있는 폴더 
│  │      origin.txt        # 각 뉴스사마다 원본 뉴스 URL
│  │      naver.txt         # naver 에서 보여주는 origin News URL 
│  │      url_clustering.py # News 회사별로 나눠주는 script 
│  │      README.md         # 전처리쪽 설명 md 파일
│  │     
│  │  Summary 코드 추가 예정  
```

## 1.2 Requirement
```bash 
if USE_PREPROCESS:
$ pip install -r requirements.txt 

if USE_DB:
$ cd DB
$ pip install -r requirements.txt
```
