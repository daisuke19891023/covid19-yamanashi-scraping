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
    def parseTable(self, soup_data):
        table = soup_data.findAll('table')[0]
        numbers = table.findAll("th")[1:]
        rows = table.findAll("tr")[1:]
        dataset = []
        for number, row in zip(numbers, rows):
            day, tmp_link = row.findAll("td")
            link = tmp_link.find('a').get('href')
            dataset.append([number.find('p').text, day.text, link])       
        return dataset

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
    print("main")