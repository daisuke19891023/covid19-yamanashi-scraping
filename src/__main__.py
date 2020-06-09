from src.scraping import Scraper
from src.statics import Statics
from src.patient import getPatientDict
from src.data_updater import DataUpdater
import datetime
if __name__ == '__main__':
    base = "https://www.pref.yamanashi.jp"
    index_html = "/koucho/coronavirus/info_coronavirus.html"
    scr = Scraper(base)
    # 発生状況等の取得
    tables_url = scr.getTargetUrl(index_html, 'info_coronavirus_data.html')
    soup = scr.getContent(tables_url)
    tables = scr.findAllTable(soup)
    # jsonファイル格納用のオブジェクト作成
    result_json = {}
    jst = datetime.timezone(
        datetime.timedelta(hours=9), name='JST')
    update_datetime = datetime.datetime.now(jst).strftime('%Y/%m/%d %H:%M')

    # 患者情報の取得
    patient_url = scr.getTargetUrl(
        index_html, 'info_coronavirus_prevention.html')
    print(patient_url)
    past_url = 'info_coronavirus_past.html'
    patients, patients_summary_data = getPatientDict(
        patient_url, past_url, scr, update_datetime)
    result_json['patients'] = patients
    result_json['patients_summary'] = patients_summary_data

    # contents, querents, inspections_summary情報の取得
    stats = Statics(base)
    contacts = stats.getStaticsDataDict(
        tables[3], "新型コロナウイルス感染症専用相談ダイヤル相談件数", update_datetime)
    result_json['contacts'] = contacts
    querents = stats.getStaticsDataDict(
        tables[2], "帰国者・接触者相談センター相談件数", update_datetime)
    result_json['querents'] = querents
    inspections_summary = stats.getStaticsDataDict(
        tables[1], "県内の疑似症例の検査状況", update_datetime)
    result_json['inspections_summary'] = inspections_summary
    result_json['lastUpdate'] = update_datetime
    # update data.json
    du = DataUpdater('data.json')
    du.update_data(result_json)
