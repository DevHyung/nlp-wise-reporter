from typing import Dict
from tqdm import tqdm
import os
def extract_n(_news):
    """

    :param _news: 신문사 도메인
    :return: 신문사 도메인에 해당하는 Naver UrlList
    """

    urlList = []
    for i, url in enumerate(originUrl):
        if _news in url:
            urlList.append(naverUrl[i])
    return urlList


def read_txt(_fileName):
    """

    :param _fileName: 읽을 파일
    :return: 빈 라인빼고 전체 Line을 List로
    """
    data = []
    with open(_fileName, 'r', encoding='utf-8') as f:
        for line in f.readlines():
            line = line.strip()
            if line != '': data.append(line)
    return data


def save_txt(_fileName, _data):
    """

    :param _fileName: 저장할 파일명
    :param _data: 저장할 데이터 1d-List
    :return: None
    """
    with open(_fileName, 'w', encoding='utf-8') as f:
        f.write('\n'.join(_data))


if __name__ == "__main__":
    # Check Dir
    BASE_DIR = './datas/'
    if not os.path.exists(BASE_DIR): os.mkdir(BASE_DIR)

    # Load Data
    originUrl = read_txt('origin.txt')
    naverUrl = read_txt('naver.txt')
    assert len(originUrl) == len(naverUrl)

    # Pre-processing
    newsDict : Dict[str, int]  = {}
    for url in originUrl:
        '''
        split('/') => ['https:', '', 'news.joins.com', 'article', 'olink', '23309016']
        idx 2 => 뉴스 URI부분
        '''
        try: newsDict[url.split('/')[2]] += 1
        except: newsDict[url.split('/')[2]] = 1
    sortedNewsList = sorted(newsDict.items(),
                     key=(lambda v : v[1]),
                     reverse=True) # Cnt 내림차순으로 정렬

    # Save
    '|왼쪽정렬|중앙정렬|'
    for idx, (k, v) in tqdm(enumerate(sortedNewsList)):
        #print("{} : {}, {}".format(idx,v, k))# 전체 뉴스가 -> 몇개씩 기사를 가지고있는지
        print("|{}|{}|{}|".format(idx, k, v))  # 전체 뉴스가 -> 몇개씩 기사를 가지고있는지

        #save_txt(BASE_DIR + "{}.txt".format(idx), extract_n(k))


