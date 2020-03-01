# Wise-Reporter / preprocessing

WiseReporter 전처리 부분 관련 코드 

## 1.1 Directory hierarchy
```bash
├─Github
│  ├─ preprocessing
│  │      datas/            # {}.txt 로 각 회사별로 URL들이 저장되어있는 폴더 
│  │      origin.txt        # 각 뉴스사마다 원본 뉴스 URL
│  │      naver.txt         # naver 에서 보여주는 origin News URL 
│  │      url_clustering.py # News 회사별로 나눠주는 script 
│  │      utils.py          # Util modules  
│  │      parser_class.py   # 기본 Parser class 상속으로 대략 42개별 파생 parser 있음
│  │      parsing.py        # Parsing하는 Main script
│  │      README.md         # 전처리쪽 설명 md 파일   
```
## 1.2 전처리 내역 (:date: 200301 작성)
```python 
if global:
    # CASE1. 문장간 띄어쓰기를 <br><br>로 보통쓰길래 \n+[SEP] 으로 바꿔줌
    # CASE2. 본문외 불필요 tag들 decompose
    removeTags = ['script', 'span', 'a', 'strong', 'td', 'b']
    # CASE3. 이메일, '재배포 금지'라는 Pattern 이 들어가있는 Line 제거
    removePattern = [r"([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)",
                     r"(\w+\s*기자)"]
    # 추가적으로 한줄 length 정해야함
    THRESHOLD = 7 

if 신문사별:
    # CASE0. 전체 TEXT에서 원하는 pattern 지우기 
    result = Remove_CASE0(result, _pattern=r"(\(서울=연합뉴스\)\s*=)")
    
    # CASE4. 원하는 Line index에서 원하는 pattern 지우기
    result = Remove_CASE4(result, _pattern=r"\[.*?\]", _idx=0)
else:
    # 좀 더 신문사별 상세한 내용은 주석으로 달아놨음
```

## 1.3 `datas/` 폴더 News Index 설명
|Index|신문사|개수|
|:---|:---:|:---:|
|0|news.joins.com|3664|
|1|yna.kr|2895|
|2|www.hankyung.com|1425|
|3|news.mt.co.kr|1400|
|4|news.kmib.co.kr|1083|
|5|news.mk.co.kr|1042|
|6|news.sbs.co.kr|924|
|7|news1.kr|887|
|8|news.jtbc.joins.com|810|
|9|news.chosun.com|804|
|10|news.kbs.co.kr|764|
|11|www.edaily.co.kr|753|
|12|view.asiae.co.kr|694|
|13|www.ytn.co.kr|686|
|14|biz.chosun.com|630|
|15|www.newsis.com|572|
|16|www.sedaily.com|568|
|17|www.hani.co.kr|544|
|18|www.segye.com|538|
|19|www.seoul.co.kr|505|
|20|imnews.imbc.com|497|
|21|news.khan.co.kr|440|
|22|www.hankookilbo.com|385|
|23|www.fnnews.com|317|
|24|news.wowtv.co.kr|310|
|25|www.donga.com|298|
|26|www.nocutnews.co.kr|238|
|27|news.donga.com|234|
|28|news.hankyung.com|221|
|29|news.heraldcorp.com|177|
|30|www.yonhapnewstv.co.kr|164|
|31|cnbc.sbs.co.kr|157|
|32|www.ichannela.com|138|
|33|moneys.mt.co.kr|129|
|34|www.ohmynews.com|126|
|35|www.dt.co.kr|123|
|36|news.tvchosun.com|113|
|37|www.etnews.com|110|
|38|www.zdnet.co.kr|94|
|39|www.inews24.com|84|
|40|www.dailian.co.kr|76|
|41|www.mbn.co.kr|63|
|42|nownews.seoul.co.kr|60|
|43|www.munhwa.com|54|
|44|www.bloter.net|35|
|45|www.xportsnews.com|34|
|46|www.pressian.com|30|
|47|www.busan.com|30|
|48|www.mediatoday.co.kr|27|
|49|news.imaeil.com|26|
|50|www.dongascience.com|16|
|51|health.chosun.com|16|
|52|www.ddaily.co.kr|14|
|53|sports.khan.co.kr|12|
|54|kormedi.com|9|
|55|biz.heraldcorp.com|8|
|56|www.joseilbo.com|8|
|57|h21.hani.co.kr|7|
|58|premium.mk.co.kr|7|
|59|mbn.mk.co.kr|7|
|60|www.sisajournal.com|6|
|61|star.mt.co.kr|6|
|62|www.womennews.co.kr|6|
|63|www.kwnews.co.kr|6|
|64|magazine.hankyung.com|4|
|65|www.sportsseoul.com|4|
|66|jmagazine.joins.com|3|
|67|game.mk.co.kr|3|
|68|weekly.donga.com|2|
|69|www.sisain.co.kr|2|
|70|newstapa.org|2|
|71|shindonga.donga.com|2|
|72|star.mk.co.kr|2|
|73|weekly.chosun.com|1|
|74|h2.khan.co.kr|1|
|75|www.tvreport.co.kr|1|
|76|sports.mk.co.kr|1|
|77|ecotopia.hani.co.kr|1|
|78|decenter.sedaily.com|1|
|79|www.newsen.com|1|
|80|www.sportsworldi.com|1|
|81|sports.donga.com|1|
|82|mirakle.mk.co.kr|1|



