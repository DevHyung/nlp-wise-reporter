from parser_class import *
from openpyxl import  load_workbook
from utils import log
from tqdm import tqdm
import os
import argparse
import json

class database:
    """ 기사 Database 저장 object """
    def __init__(self, firstDate, finalDate, naverUrl, originalUrl,
                        originalTitle, category, crawlDate, originalHTML, result=''):
        self.firstDate = firstDate
        self.finalDate = finalDate
        self.naverUrl = naverUrl
        self.originalUrl = originalUrl
        self.originalTitle = originalTitle
        self.category = category
        self.crawlDate = crawlDate
        self.originalHTML = originalHTML
        self.result = result


def parse_option():
    """ argparser 부분 """
    option = argparse.ArgumentParser(description='WiseReporter Preprocess')
    option.add_argument('--input_excel', type=str, required=True, help='DB Pull 결과물')
    option.add_argument('--output_json', type=str, required=True, help='결과물 JSON 파일 이름')
    option.add_argument('--line_min', type=int, default=7, help='한 줄 최소 길이')
    option.add_argument('--summary_min', type=int, default='false', help='원본 HTML 포함 할 지')
    option.add_argument('--include_html', type=str, default='false', help='원본 HTML 포함 할 지')
    return option.parse_args()


def load_excel(_fileName):
    """
    엑셀 읽어서 DB클래스 generator object로 반환 !
    :param _fileName: 엑셀파일 argument 이름
    :return: database class generator
    """
    wb = load_workbook(filename=_fileName)
    sheet = wb.active
    isFirst = True
    datas = []
    for i in sheet.rows:
        if isFirst: # 첫줄 제거
            isFirst = False
            continue
        firstDate = i[0].value
        finalDate = i[1].value
        naverUrl = i[2].value
        originalUrl = i[3].value
        originalTitle = i[4].value
        category = i[5].value
        crawlDate = i[6].value
        originalHTML = i[7].value
        if originalUrl == None or originalHTML == None:# 하나라도 없으면
            break
        else:
            # For Generator version : 속도는 빠르긴한데 언제끝나는지 예측이안됨
            # yield database(firstDate, finalDate, naverUrl, originalUrl,
            #               originalTitle, category, crawlDate, originalHTML)

            datas.append(database(firstDate, finalDate, naverUrl, originalUrl,
                           originalTitle, category, crawlDate, originalHTML)
                         )# For List version

    return  datas # For List version

def post_processing(_text):
    """
    기타 추가 후처리 하는 부분
    1. Line min값 적용해서 아닌부분 지우기
    2. 요약문, 본문 나눠줌
        2.1 요약문의 길이 제한을 두자
    3. 요약문에 동영상 뉴스가 포함되어있는지 본다
    :return: 뉴스타입, 요약문, 본문
    """
    type ='news' # news, video

    # 1. Line min 값 해서 이상인 부분만 추출하기
    lines = []
    for line in _text.strip().replace('\n', '').split('[SEP]'):
        line = line.strip()
        if line != '':
            if len(line) >= args.line_min:
                lines.append(line.strip())

    # 2. 요약문 legnth 제한 만큼 뽑고
    #    본문 나눠줌
    summaryIdx = -1
    charCnt = 0
    for idx, sentence in enumerate(lines):
        if charCnt > args.summary_min:
            summaryIdx = idx
            break
        charCnt += len(sentence)
    summary = '\n'.join(lines[:summaryIdx])
    content = '\n'.join(lines[summaryIdx:])

    # 3. 동영상뉴스파악
    if '동영상 뉴스' in summary:
        type = 'video'
    return type, summary, content


def init_dict():
    """ 저장할 dict 초기화 """
    return {
            'input_excel' : args.input_excel,
            'total_cnt' : '',
            'remove_cnt': 0,
            'datas' : []
            }


def make_article_dict(_data: database, type, _summary, _content):
    """

    :param _data: 엑셀 한줄 database object
    :param _summary: 요약문
    :param _content: 본문
    :return: 1개의 기사 dictionary
    """
    resultDict = {}
    try:    resultDict['firstDate'] = _data.firstDate.strftime("%Y-%m-%d %H:%M:%S")
    except: resultDict['firstDate'] = ''
    try:    resultDict['finalDate'] = _data.finalDate.strftime("%Y-%m-%d %H:%M:%S")
    except: resultDict['finalDate'] = ''
    resultDict['type'] = type
    resultDict['crawlDate'] = str(_data.crawlDate)
    resultDict['naverUrl'] = _data.naverUrl
    resultDict['originalUrl'] = _data.originalUrl
    resultDict['category'] = _data.category
    resultDict['originalTitle'] = _data.originalTitle
    resultDict['summary'] = _summary
    resultDict['summary_len'] = len(_summary)
    resultDict['content'] = _content
    resultDict['content_Len'] = len(_content)
    if args.include_html.lower() == 'true':
        resultDict['html'] = _data.originalHTML
    return resultDict



if __name__ == "__main__":
    # Args parse
    args = parse_option()
    if 'preprocessing' not in os.getcwd():
        # shell로 이 파일 바로 실행하면 경로가 빠질수도
        os.chdir(os.getcwd()+'/preprocessing')
    resultDict = init_dict() # 결과저장할 Dict 초기화

    # Excel Load
    datas: database = load_excel(args.input_excel)

    # Preprocess
    for data in tqdm(datas):
        # Parser class instance
        parser = make_parser(data.originalUrl)
        # Article class instance
        article = Article(_urlTuple=('', ''), #소스코드 있을떈 urlTuple 비우기 (초기화 되어있어서 빼도 됨)
                          _html = data.originalHTML)
        # Parsing
        if parser is not None:
            isComplete = parser.parsing(article)
            if isComplete:
                type, summary, content = post_processing(article.get_result())
                resultDict['datas'].append(make_article_dict(data, type, summary, content))
                if len(summary) == 0: resultDict['remove_cnt'] += 1
            else:
                log('e', 'parsing error')
    resultDict['total_cnt'] = len(resultDict['datas'])

    # Save
    with open(args.output_json, 'w', encoding='utf-8') as file:
        json.dump(resultDict,
                  file,
                  ensure_ascii=False,
                  indent='\t')






