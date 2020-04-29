import os
import re
import datetime


from itertools import groupby

from src.lib.pdf2text import Pdf2Text
from src.lib.parserPdf import ParserPdf
from src.lib.common_util import StringUtil, TimeUtil, PathOperater


def getPatientDict(index_html, scr):
    # 発生状況等の取得
    url = scr.getTargetUrl(index_html, 'info_coronavirus_prevention.html')
    soup = scr.getContent(url)
    # テーブル情報を取得する
    dataset = scr.parseSingleTable(soup)

    # pdf格納folderの作成
    pathOp = PathOperater()
    pathOp.createPath('pdf')

    # 県外事例は除外
    inside_checker = StringUtil()
    patient_data_tmp = []
    patients_summary_tmp = []
    for data in dataset:
        if inside_checker.exclude_outside(data[0]):

            # 格納先のファイル名を作成
            file_name = pathOp.setDownlaodFileName(
                'pdf', pathOp.getFileName(data[3]))
            scr.downloadPdf(data[3], file_name)
            output_file = os.path.splitext(os.path.basename(file_name))[0]
            output_path = os.path.join('./text', output_file + '.txt')
            isDuplicated, number_char = StringUtil().is_duplicate_data(data[0])

            # 重複している場合
            if isDuplicated:
                for n in number_char:
                    #print('No:{} リリース日:{} 判明日:{} Link:{}'.format(n, data[1].strip(), data[2].strip(), output_path))
                    patient_data_tmp.append(
                        {"No": n, "リリース日": data[1].strip(), "link": output_path})
                    patients_summary_tmp.append(data[2].strip())

            # 単一の場合
            else:
                #print('No:{} リリース日:{} 判明日:{} Link:{}'.format(number_char, data[1].strip(), data[2].strip(), output_path))
                patient_data_tmp.append(
                    {"No": number_char, "リリース日": data[1].strip(), "link": output_path})
                patients_summary_tmp.append(data[2].strip())

    # convertの実行
    pathOp.createPath('text')
    convert_txt = Pdf2Text()
    convert_txt.executeConvert()

    # テキストからjsonの作成
    parser = ParserPdf()
    patient_list = []

    # patientの作成
    for tmp in patient_data_tmp:
        result = parser.text2dict(tmp['No'], tmp['link'])
        result.update(tmp)
        result.update({'退院': None})
        del result['link']
        patient_list.append(result)
    patients = {}
    patients['data'] = sorted(patient_list, key=lambda x: int(
        re.sub(r'県|内|例|目', '', x['No'])))
    patients['__comments'] = "陽性患者の属性"

    # patients_summaryの作成
    patients_summary_data = {}
    patients_summary_data['__comments'] = "陽性患者数"
    patients_summary = TimeUtil().createDatetimeDict(datetime.datetime.now())
    for k, g in groupby(patients_summary_tmp):
        patients_summary = list(map(lambda x: {"日付": x["日付"], "小計": len(
            list(g)) if x['日付'] == k else x['小計']}, patients_summary))

    patients_summary_data['data'] = sorted(
        patients_summary, key=lambda x: x['日付'])

    return patients, patients_summary_data
