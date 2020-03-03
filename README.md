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
│  │      parser_class.py   # 기본 Parser class 상속으로 대략 42개별 파생 parser 있음
│  │      parsing.py        # Parsing하는 Main script
│  │      parsing.sh        # 실행 쉘 스크립트 
│  │      url_clustering.py # News 회사별로 나눠주는 script  
│  │      utils.py          # Util modules
│  │      sample.xlsx       # 샘플 Input   
│  │      sample_result.json# 샘플 Output    
│  │      README.md         # 전처리쪽 설명 md 파일  
```

## 1.2 Requirement
```bash 
$ pip install -r requirements.txt 
```
