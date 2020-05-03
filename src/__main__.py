import json
from src.scraping import Scraper
from src.statics import getStaticsDataDict
from src.patient import getPatientDict
from src.create_data import create_data
import datetime
if __name__ == '__main__':
    base = "https://www.pref.yamanashi.jp"
    index_html = "/koucho/coronavirus/info_coronavirus.html"
    scr = Scraper(base)
    # 発生状況等の取得
    url = scr.getTargetUrl(index_html, 'info_coronavirus_data.html')
    soup = scr.getContent(url)
    tables = scr.findAllTable(soup)
    # jsonファイル格納用のオブジェクト作成
    result_json = {}
    jst = datetime.timezone(
        datetime.timedelta(hours=9), name='JST')
    update_datetime = datetime.datetime.now(jst).strftime('%Y/%m/%d %H:%M')
    result_json['lastUpdate'] = update_datetime

    # 患者情報の取得
    patients, patients_summary_data = getPatientDict(index_html, scr)
    patients.update({'date': update_datetime})
    patients_summary_data.update({'date': update_datetime})
    result_json['patients'] = patients
    result_json['patients_summary'] = patients_summary_data

    # ontents, querents, inspections_summary情報の取得
    contacts = getStaticsDataDict(scr, tables[3], "新型コロナウイルス感染症専用相談ダイヤル相談件数")
    contacts.update({'date': update_datetime})
    result_json['contacts'] = contacts
    querents = getStaticsDataDict(scr, tables[2], "帰国者・接触者相談センター相談件数")
    querents.update({'date': update_datetime})
    result_json['querents'] = querents
    inspections_summary = getStaticsDataDict(scr, tables[1], "県内の疑似症例の検査状況")
    inspections_summary.update({'date': update_datetime})
    result_json['inspections_summary'] = inspections_summary

    create_data(result_json)
