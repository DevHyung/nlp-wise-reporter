# Wise-Reporter / preprocessing

WiseReporter 전처리 부분 관련 코드 

## 1.1 Directory hierarchy
```bash
├─Github
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

## 1.3 Usage 
```shell script
1. Run shell script 
$./parsing.sh

2. 또는 
>vi parsing.sh
PYTHON=/Users/hjpark/Desktop/dev/bin/python3 # 파이썬 경로
${PYTHON} parsing.py \
  --input_excel sample.xlsx\                 # DB에서 가져온 Input xlsx 파일 
  --output_json sample_result.json\          # 결과물 저장 파일 (기본 JSON형식)
  --line_min 7\                              # 한줄의 최소 길이 
  --summary_min 30\                          # 요약문의 최소 길이
  --include_html false\                      # HTML코드 포함저장 t/f

수정후 실행
```

## 1.4 Result Key Description  
```json
{
	"input_excel": "sample.xlsx",         # 입력파일이름  
	"total_cnt": 5,                       # 총 개수 
	"remove_cnt": 0,                      # Parser 클래스에 없는 신문사 or 본문들이 remove tags 들로만 이루어진 걸러진 기사 수 
	"datas": [
		{
			"firstDate": "2019-01-01 09:34:59", 
			"finalDate": "2019-01-01 11:38:00",
			"type": "news",               # 일반 = News, 동영상 뉴스 = video
			"crawlDate": "20190101",
			"naverUrl": "NAVER_URL",
			"originalUrl": "http://yna.kr/AKR20190101021552504?did=1195m",
			"category": "정치",
			"originalTitle": "北김정은 \"조선반도 항구적 평화지대로 만들려는 확고한 의지\"(종합)", # 제목
			"summary": "오전 9시부터 방송 통해 신년사 발표\"우리 주동적 노력으로 조선반도에 평화기류\"",
			"summary_len": 44,          
			"content": "김정은 북한 국무위원장이 1일 신년사를 통해 \"조선반도(한반도)를 항구적 평화지대로 만들려는 확고한 의지\"가 있다고 밝혔다.\n김 위원장은 이날 오전 9시부터 조선중앙를 통해 녹화 중계로 발표한 신년사에서 \"우리의 주동적이면서도 적극적인 노력에 의하여 조선반도(한반도)에서 평화에로 향한 기류\"가 형성됐다며 이같이 평가했다.\n김 위원장은 \"민족의 화해와 단합, 평화번영의 새 역사를 써 나가기 위하여 우리와 마음을 같이 한 남녘 겨레들과 해외 동포들에게 따뜻한 새해 인사를 보낸다\"고도 말했다.\n김 위원장은 국내 경제와 관련해서는 \"노동당 시대를 빛내이기 위한 방대한 대건설사업들이 입체적으로 통이 크게 전개됨으로써 그 어떤 난관 속에서도 끄떡없이 멈춤이 없으며 더욱 노도와 같이 떨쳐 일어나 승승장구해 나가는 사회주의 조선의 억센 기상과 우리의 자립경제의 막강한 잠재력이 현실로 과시되었다\"고 주장했다.\n그러면서 \"조선혁명의 전 노정에서 언제나 투쟁의 기치가 되고 비약의 원동력으로 되어온 자력갱생을 번영의 보검으로 틀어쥐고 사회주의 건설의 전 전선에서 혁명적 앙양을 일으켜 나가야 한다\"며 \"사회주의 자립경제의 위력을 더 강화해야 한다\"고 거듭 강조했다.\n김 위원장은 2013년부터 매년 육성으로 신년사를 발표해 왔다.\n특히 올해는 중앙가 이례적으로 김 위원장이 양복 차림으로 신년사 발표를 위해 노동당 중앙청사에 입장하는 장면부터 공개했고, 김창선 국무위원장 부장이 맞이했으며 김여정 당 제1부부장, 조용원 당 부부장 등 김 위원장의 최측근 인사들이 뒤따라 들어왔다.\n또 김 위원장은 단상에서 신년사를 발표하던 것과 달리 올해는 김일성 주석의 사진이 걸린 집무실로 보이는 장소의 소파에 앉아 신년사를 읽어내려가 눈길을 끌었다.\n2013년부터 2015년까지는 오전 9시께 조선중앙 등을 통해 김정은 신년사 프로그램이 녹화 방송됐다.\n2016년과 2017년에는 낮 12시 30분(평양시 기준 낮 12시)에 신년사가 방송됐고, 지난해에는 오전 9시 30분(평양시 기준 오전 9시)에 발표됐다.\n김 위원장의 신년사는 새해 분야별 과업을 제시하면서 통상 대내정책, 대남메시지, 대외정책 등의 순으로 구성되는데, 신년사에서 제시된 과업은 북한에선 반드시 집행해야 하는 절대적인 지침으로 여겨진다.",
			"content_Len": 1113
		},
        ...
      }
    ]
}
```

## 1.5 `datas/` 폴더 News Index 설명
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



