from scraping import Scraper, PathOperater
from pdf2text import Pdf2Text
from parserPdf import ParserPdf
import glob
import json
import os
from common_util import StringUtil, TimeUtil
from itertools import groupby
import datetime
if __name__ == '__main__':
    base = "https://www.pref.yamanashi.jp"
    index_html= "/koucho/coronavirus/info_coronavirus.html"
    scr = Scraper(base)
    # 発生状況等の取得
    url2 = scr.getTargetUrl(index_html, 'info_coronavirus_prevention.html')
    print(url2)
    soup2 = scr.getContent(url2)
    #テーブル情報を取得する
    dataset = scr.parseSingleTable(soup2)

    #pdf格納folderの作成
    pathOp = PathOperater()
    pathOp.createPath('pdf')
    #県外事例は除外
    inside_checker = StringUtil()
    patient_data_tmp= []
    patients_summary_tmp = []
    for data in dataset:
        if inside_checker.exclude_outside(data[0]):

            # 格納先のファイル名を作成
            file_name = pathOp.setDownlaodFileName('pdf', pathOp.getFileName(data[3]))
            scr.downloadPdf(data[3], file_name)
            output_file = os.path.splitext(os.path.basename(file_name))[0]
            output_path = os.path.join('./text', output_file + '.txt')
            print('No:{} リリース日:{} 判明日:{} Link:{}'.format(data[0], data[1].strip(), data[2].strip(), output_path))
            patient_data_tmp.append({"No":data[0], "リリース日":data[1].strip(), "link": output_path})
            patients_summary_tmp.append(data[2].strip())
            
    text_tmp = json.dumps(patient_data_tmp,indent=4,ensure_ascii=False)
    with open('./data_tmp.json', "wb") as f:
        f.write(text_tmp.encode('utf-8', "ignore"))    
    #convertの実行
    convert_txt = Pdf2Text()
    convert_txt.executeConvert()

    #テキストからjsonの作成
    parser = ParserPdf()
    json_list = []

    #patientの作成
    for tmp in patient_data_tmp:
        result = parser.text2dict(tmp['link'])
        result.update(tmp)
        del result['link']
        json_list.append(result)
    patients = {}
    patients['data'] = json_list
    patients['__comments'] = "陽性患者の属性"

    #patients_summaryの作成
    patients_summary_data = {}
    patients_summary_data['__comments'] = "陽性患者数"
    patients_summary = TimeUtil().createDatetimeDict(datetime.datetime.now())
    for k, g in groupby(patients_summary_tmp):
        patients_summary = list(map(lambda x: {"日付":x["日付"], "小計":len(list(g)) if x['日付'] == k else x['小計']}, patients_summary))

    print(patients_summary)
    patients_summary_data['data'] = sorted(patients_summary,key=lambda x:x['日付'])

    #jsonファイルへの書き出し
    result_json = {}
    result_json['patient'] = patients   
    result_json['patients_summary'] = patients_summary_data
    text = json.dumps(result_json,indent=4,ensure_ascii=False)
    with open('./data.json', "wb") as f:
        f.write(text.encode('utf-8', "ignore"))




