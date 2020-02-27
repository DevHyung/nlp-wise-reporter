from utils import read_txt, log
from typing import List, Tuple
from bs4 import BeautifulSoup
import re
import requests

##### CONFIG AREA START
CUSTOM_HEADER = {'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.106 Safari/537.36'}
BASE_DIR = './datas/'
NAVER_IDX = 0
ORIGIN_IDX = 1
REMOVE_TAGS = ['script', 'span', 'a', 'strong', 'td', 'b']
REMOVE_PATTERN = [r"([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)",
                         r"(재배포\s*금지)"] # 한 라인을 날려버리는
##### CONFIG AREA END


class Article:
    def __init__(self, _urlTuple, _html=''):
        self.naverUrl ,self.originUrl = _urlTuple # ( Naver URL, 원본 URL )
        self.html: str = _html
        self.title: str = ''
        self.content: BeautifulSoup = ''
        self.result: str = ''
        self.isRemove = False
        if _html == '':
            self.html = self.requests_html()

    def requests_html(self):
        resp = requests.get(self.naverUrl, headers=CUSTOM_HEADER)
        log('s', "GET - {}".format(self.naverUrl))
        return resp.text

    def show_result(self): # 요약문 HTML 을 보여주는 함수
        """
        self.result 가 str 상태로 [SEP] 구분자로
        나눠져있다고 가정
        :return:
        """
        result = self.result.replace('\n','')

        lineList = []
        for line in result.split('[SEP]'):
            if line.strip() != '':
                lineList.append(line.strip())
        result = '\n\n'.join(lineList)
        print(result)


    # Getter
    def get_domain(self): return self.originUrl
    def get_url(self): return self.naverUrl
    def get_html(self): return self.html
    def get_isRemove(self): return self.isRemove
    def get_result(self): return self.result

    # Setter
    def set_title(self,_title): self.title = _title
    def set_content(self, _content): self.content = _content
    def set_result(self, _result): self.result = _result
    def set_isRemove(self, _isRemove): self.isRemove = _isRemove


class BaseParser:
    def __init__(self):
        self.idx = -1
        self.domain = ''

    def __str__(self): # repr은 쓸필요없을것같아 이거로 대체
        return "[{}] idx '{}' parser".format(self.idx, self.domain)

    def general_parsing(self, _article: Article):
        # Conver HTML -> BS4 Object
        bs = BeautifulSoup(_article.get_html(), 'lxml')

        # Article area 부분 catch
        content = bs.find('div', id='main_content')

        # Head title ( div > h3 )
        head = content.find('div', class_='article_header')
        try:
            title = head.find('h3', id='articleTitle').text.strip()
            _article.set_title(title)
        except:# 이경우에 들어오는건 기사가 삭제되었다는거
            log('e', "삭제된기사 : {}".format(_article.get_url()))
            _article.set_isRemove(True)
            return 0

        # Body
        # CASE1. 문장간 띄어쓰기를 <br><br>로 보통쓰길래 \n+[SEP] 으로 바꿔줌
        # CASE2. 본문외 불필요 tag들 decompose
        # CASE3. 이메일, '재배포 금지'라는 Pattern 이 들어가있는 Line 제거
        body = content.find('div', id='articleBodyContents')

        """ CASE1 START"""
        br_modify: str = str(body).replace('<br/> <br/>', '<br/><br/>')
        br_modify: str = br_modify.replace('<br/><br/>', '\n[SEP]\n')
        remove_case1 = BeautifulSoup(br_modify, 'lxml')
        _article.set_content(remove_case1) # 1차정제본을 원본으로 가정
        """ CASE1 END"""

        """ CASE2 START """
        for tag in REMOVE_TAGS:
            tagNum = len(remove_case1.find_all(tag))
            for _ in range(tagNum):
                try: remove_case1.find(tag).decompose()
                except: pass
        remove_case2 = remove_case1
        """ CASE2 END """

        """ CASE3 START """
        removeList = []
        remove_case2_list = remove_case2.text.split('[SEP]')
        compilePattern = [ re.compile(pt) for pt in REMOVE_PATTERN ]
        for line in remove_case2_list:
            for cpt in compilePattern:
                if cpt.search(line) != None: # 매칭
                    removeList.append(line)
                    break
        for r in removeList: remove_case2_list.remove(r)
        remove_case3: str = "[SEP]".join(remove_case2_list)
        """ CASE3 END """

        _article.set_result(remove_case3)
        return 1
    def post_edit(self, _text): # Base 에는 적용 X
        # 김창우 기자 같은 패턴 제거해버리기
        subPattern = [r"(\w+\s*기자)",
                         r'[@#※ㆍ!』…》▶ⓒ◆◇▲©○]', ]
        for pt in subPattern:
            _text = re.sub(pt, '', _text)
        return _text

class NewsJoins(BaseParser):
    def __init__(self):
        self.idx = 0  # 0번째 뉴스 신문사
        self.domain = 'news.joins.com'

    def parsing(self, _article: Article):
        super().general_parsing(_article)
        base_result = _article.get_result()
        result = super().post_edit(base_result)
        _article.set_result(result)
        return 1


class Yna(BaseParser):
    def __init__(self):
        self.idx = 1  # 0번째 뉴스 신문사
        self.domain = 'yna.kr'

    def parsing(self, _article: Article):
        super().general_parsing(_article)

def make_parser(_originUrl)-> Article:
    news = _originUrl.split('/')[2].strip()
    parser = None
    if news == 'news.joins.com':
        parser = NewsJoins()
    elif news == 'yna.kr':
        parser = Yna()

    log('s',"Loading ... {}".format(parser))
    return parser


def load_url_by_file(_fileNum) -> List[Tuple[str, str]]:
    """
    File로 부터 신문사들 URL가져옮

    :param _fileNum: 뉴스언론사 index
    :return: zip(naver url, origin url)
    """
    urldatas = read_txt(BASE_DIR + "{}.txt".format(_fileNum))  # naver @@@ origin
    # (naver, origin)
    urlList = list(zip(
                    [url.split('@@@')[NAVER_IDX] for url in urldatas],
                    [url.split('@@@')[ORIGIN_IDX] for url in urldatas]
                    ))
    log('s', "{}.txt 파일에서 {}개 불러옴... Ex) {} ".format(_fileNum, len(urlList), urlList[0][ORIGIN_IDX]))
    return urlList
