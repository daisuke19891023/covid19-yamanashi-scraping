from src.lib.json_checker import JsonChecker
from src.scraping import Scraper


class Statics:
    def __init__(self, base_url: str):
        self.scr = Scraper(base_url)

    def getStaticsDataDict(self, table, comments: str, update_datetime_iso: str) -> dict:
        res_dict = self.scr.parseContactsTable(table)

        # jsonへの格納
        dictonary = {}
        dictonary['__comments'] = comments
        dictonary['date'] = update_datetime_iso

        # 小計が0とならない最新の日付までのリストにする
        jc = JsonChecker()
        data = sorted(res_dict, key=lambda x: x['日付'])
        data = jc.exclude_zero_max_date(data)
        dictonary['data'] = data

        return dictonary
