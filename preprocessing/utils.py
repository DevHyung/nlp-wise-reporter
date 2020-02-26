def log(_option, _msg):
    if   _option.lower() == 'e': print("[Error]   : {}".format(_msg))
    elif _option.lower() == 's': print("[Success] : {}".format(_msg))
    elif _option.lower() == 'i': print("[Info]    : {}".format(_msg))

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
