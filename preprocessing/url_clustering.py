from typing import Dict
from tqdm import tqdm
from preprocessing.utils import read_txt, save_txt
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
    for idx, (k, v) in tqdm(enumerate(sortedNewsList)):
        #print("{} : {}, {}".format(idx,v, k)) # 전체 뉴스가 -> 몇개씩 기사를 가지고있는지
        #print("|{}|{}|{}|".format(idx, k, v)) # for README
        save_txt(BASE_DIR + "{}.txt".format(idx), extract_n(k))


