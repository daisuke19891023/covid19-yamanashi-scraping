import requests
import re

from bs4 import BeautifulSoup

from src.lib.time_util import TimeUtil


class Scraper:
    def __init__(self, base):
        self.base = base
        self.time_util = TimeUtil()

    def getTargetUrl(self, base_url: str, target_url: str):
        r = requests.get(self.base + base_url)
        r.encoding = r.apparent_encoding
        soup = BeautifulSoup(r.text, 'html.parser')
        elems = soup.find(href=re.compile(target_url))
        return elems.get('href')

    def getContent(self, url: str):
        r = requests.get(self.base + url)
        r.encoding = r.apparent_encoding
        return BeautifulSoup(r.text, 'html.parser')

    def downloadPdf(self, pdf_url: str, path_name: str) -> None:
        r = requests.get(self.base + pdf_url, stream=True)
        with open(path_name, 'wb') as fd:
            for chunk in r.iter_content(chunk_size=2000):
                fd.write(chunk)

    def parseSingleTable(self, soup_data):
        table = soup_data.findAll('table')[0]
        numbers = table.findAll("th")[1:]
        rows = table.findAll("tr")[1:]
        dataset = []
        for number, row in zip(numbers, rows):
            day_proved, tmp = row.findAll("td")
            # dayにpタグが付いているパターンがある
            correct_date = tmp.findAll('a')[-1]
            day_release = correct_date.getText()
            try:
                ad_day_release = self.time_util.convert_wareki_to_ad(
                    day_release.strip())
                ad_day_proved = self.time_util.convert_wareki_to_ad(
                    day_proved.text.strip())
            except ValueError as e:
                raise e

            link = correct_date.get('href')

            dataset.append(
                [number.find('p').text, ad_day_release, ad_day_proved, link])
        return dataset

    def findAllTable(self, soup_data):
        return soup_data.findAll('table')

    def parseContactsTable(self, table):
        def convertDaysCountKV(texts):
            result = []
            for text in texts:
                # 5月1日など月が記載されている箇所があるため、月以前を削除する
                if re.search(r'月', text) is not None:
                    _, text = re.split(r'月', text)
                # 誤字で日が件と表示されている箇所があるため、日と件の両方で分割
                key, count, *_ = re.split(r'日|件', text)
                result.append({'day': int(key), 'count': int(count)})
            return result

        items = table.findAll('tr')[1:]
        res_dict = []
        for item in items:
            # span
            # td属性からテキストを取得
            span, sum_number_tmp, individuals_tmp = item.findAll('td')
            # sum_number = sum_number_tmp.findAll('p')[0]
            individuals = list(individuals_tmp.findAll('p')
                               [0].text.strip().split('、'))

            # spanからreturnするdictonaryのlistを取得する
            target_list = TimeUtil().get_dt_dict_from_text(span.text.strip())

            # 日ごとの件数をkvで取得
            days_count_dict = convertDaysCountKV(individuals)

            for day_count in days_count_dict:

                target_list = list(map(lambda x: {
                                   '日付': x['日付'], '小計': day_count['count'] if x['day'] == day_count['day'] else x['小計'], 'day': x['day']}, target_list))

            res_dict.extend(target_list)
        # 一次変数の'day'を消して返却
        return list(map(lambda x: {'日付': x['日付'], '小計': x['小計']}, res_dict))


if __name__ == '__main__':
    print("main")
