from parser_class import *
import os

if __name__ == "__main__":
    if 'preprocessing' not in os.getcwd(): # For Pycharm .idea로 하면 오류가 생길수도있음
        os.chdir(os.getcwd()+'/preprocessing')

    # Load Url List
    # (naver url, origin url)
    NEWS_IDX = 0  # 언론사
    URL_NUM = 3   # URL 인덱스
    urlList: List[ Tuple[str,str] ] = load_url_by_file(NEWS_IDX)

    # Article class instance
    # Page Source 코드가 있으면 뒤에 주면됨 기본값이 ''
    article = Article(urlList[URL_NUM])

    # Parser class instance
    parser = make_parser(urlList[URL_NUM][ORIGIN_IDX])

    if parser is not None:
        # Parsing
        isComplete = parser.parsing(article)
        if isComplete:
            article.show_result()
        else:
            log('e', 'parsing error')
    else:
        log('e', 'parser load error')