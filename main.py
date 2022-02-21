import urllib.request

import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib.error import URLError, HTTPError
import pandas as pd
import requests
from datetime import datetime

def get_href(soup):
    # 각 분야별 속보 기사에 접근할 수 있는 href를 리스트로 반환

    result = []

    div = soup.find("div", class_="list_body newsflash_body")

    for dt in div.find_all("dt", class_="photo"):
        result.append(dt.find("a")["href"])
    return result

def get_request(section, page):
    custom_header = {
        'referer' : 'https://www.naver.com/',
        'user-agent' : 'Mozilla/5.0 (Macintosh; Intel Max OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'
    }
    url = "https://news.naver.com/main/list.nhn"

    sections = {
        "정치" : 100,
        "경제" : 101,
        "사회" : 102,
        "생활" : 103,
        "세계" : 104,
        "과학" : 105
    }

    req = requests.get(url, headers=custom_header,
                       params={"sid1": sections[section], "page":page})
    return req

def main():
    custom_header = {
        'referer': 'https://www.naver.com/',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Max OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'
    }
    list_href = []
    section = input("정치, 경제, 사회, 생활, 세계, 과학 중 하나를 입력 > ")
    #섹션을 입력
    df_title = []
    df_content = []
    for i in range(20):

        req = get_request(section, i+1)
        soup = BeautifulSoup(req.text, "html.parser")

        list_href = get_href(soup)
        for j in range(len(list_href)):
            url = list_href[j]
            req = requests.get(url, headers=custom_header)
            soup = BeautifulSoup(req.text, "html.parser")
            try:
                title = soup.select('h3#articleTitle')[0].text.replace("\n","").replace("\t","")
                content = soup.select('#articleBodyContents')[0].get_text().replace("\n","").replace("\t","")
                df_title.append(title + "\n\n\n")
                df_content.append(content + "\n\n\n")
            except:
                print("e")
    data = {
        'title': df_title,
        'content' : df_content
    }
    df = pd.DataFrame(data)
    df.to_csv('./data/'+section+'.csv', index=False, mode='a', encoding='utf-8')

if __name__ == "__main__":
    main()




