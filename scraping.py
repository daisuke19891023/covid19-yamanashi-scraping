import requests
from bs4 import BeautifulSoup
import re
import os

class Scraper:
    def __init__(self, base):
        self.base = base
    def getTargetUrl(self, base_url, target_url):
        r = requests.get(self.base + base_url)
        r.encoding = r.apparent_encoding
        soup = BeautifulSoup(r.text, 'html.parser')
        elems = soup.find(href=re.compile(target_url))
        return elems.get('href')
    def getContent(self, url):
        r = requests.get(self.base + url)
        r.encoding = r.apparent_encoding
        return BeautifulSoup(r.text, 'html.parser')
    def downloadPdf(self, pdf_url, path_name):
        r = requests.get(self.base + pdf_url, stream=True)
        with open(path_name, 'wb') as fd:
            for chunk in r.iter_content(chunk_size=2000):
                fd.write(chunk)

class PathOperater:
    def __init__(self):
        self.current= os.getcwd()
    def createPath(self, path_name):
        target_path = os.path.join(self.current, path_name)
        if(os.path.exists(target_path)):
            return 0
        else:
            os.makedirs(target_path)
    def getFileName(self, url_file_path):
        return os.path.basename(url_file_path)
    def setDownlaodFileName(self, path, fileName):
        return os.path.join(self.current, path, fileName)

if __name__ == '__main__':
    base = "https://www.pref.yamanashi.jp"
    index_html= "/koucho/coronavirus/info_coronavirus.html"
    scr = Scraper(base)
    # 発生状況等の取得
    url2 = scr.getTargetUrl(index_html, 'info_coronavirus_prevention.html')
    print(url2)
    soup2 = scr.getContent(url2)
    #テーブル情報を取得する
    table = soup2.findAll('table')[0]
    rows = table.findAll("tr")[1:]
    for row in rows:
        day = row.findAll("td")[0]
        print(day)

    exit()
    elems = soup2.findAll(href=re.compile('pdf'),text=re.compile('報道資料'))
    print(len(elems))
    #pdf格納folderの作成
    pathOp = PathOperater()
    pathOp.createPath('pdf')
    for e in elems:
        print('{}:{}'.format(e.getText(),e.get('href')))
        # 格納先のファイル名を作成
        file_name = pathOp.setDownlaodFileName('pdf', pathOp.getFileName(e.get('href')))
        scr.downloadPdf(e.get('href'), file_name)


