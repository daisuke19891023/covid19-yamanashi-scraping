import json
from scraping import Scraper
from statics import getStaticsDataDict
from patient import getPatientDict
if __name__ == '__main__':
    base = "https://www.pref.yamanashi.jp"
    index_html= "/koucho/coronavirus/info_coronavirus.html"
    scr = Scraper(base)
    # 発生状況等の取得
    url = scr.getTargetUrl(index_html, 'info_coronavirus_data.html')
    soup = scr.getContent(url)
    tables = scr.findAllTable(soup)


    #jsonファイル格納用のオブジェクト作成
    result_json = {}

    #患者情報の取得
    patients, patients_summary_data = getPatientDict(index_html, scr)
    result_json['patient'] = patients   
    result_json['patients_summary'] = patients_summary_data

    #contents, querents, inspections_summary情報の取得
    result_json['contacts'] = getStaticsDataDict(scr, tables[3], "新型コロナウイルス感染症専用相談ダイヤル相談件数")
    result_json['querents'] = getStaticsDataDict(scr, tables[2], "帰国者・接触者相談センター相談件数")
    result_json['inspections_summary'] = getStaticsDataDict(scr, tables[1], "県内の疑似症例の検査状況")



    text = json.dumps(result_json,indent=4,ensure_ascii=False)
    with open('./data.json', "wb") as f:
        f.write(text.encode('utf-8', "ignore"))