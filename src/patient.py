import os
import re
import datetime


from itertools import groupby

from src.lib.pdf_parser import PdfParser
from src.lib.text_parser import TextParser
from src.lib.string_util import StringUtil
from src.lib.path_operator import PathOperator
from src.lib.time_util import TimeUtil
from src.lib.json_checker import JsonChecker


def getPatientDict(index_html, scr, update_datetime):
    # 発生状況等の取得
    url = scr.getTargetUrl(index_html, 'info_coronavirus_prevention.html')
    soup = scr.getContent(url)
    # テーブル情報を取得する
    try:
        dataset = scr.parseSingleTable(soup)
    except ValueError as e:
        raise e
    # pdf格納folderの作成
    path_op = PathOperator()
    path_op.create_path('pdf')

    # 県外事例は除外
    inside_checker = StringUtil()
    patient_data_tmp = []
    patients_summary_tmp = []
    for data in dataset:
        if inside_checker.exclude_outside(data[0]):

            # 格納先のファイル名を作成
            file_name = path_op.set_downlaod_file_name(
                'pdf', path_op.get_file_name(data[3]))
            scr.downloadPdf(data[3], file_name)
            output_file = os.path.splitext(os.path.basename(file_name))[0]
            output_path = os.path.join('./text', output_file + '.txt')
            is_duplicated, number_char = StringUtil(
            ).is_duplicate_data(data[0])

            # 重複している場合
            if is_duplicated:
                for n in number_char:
                    # print('No:{} リリース日:{} 判明日:{} Link:{}'.format(n, data[1].strip(), data[2].strip(), output_path))
                    patient_data_tmp.append(
                        {"No": n, "リリース日": data[1].strip(), "link": output_path})
                    patients_summary_tmp.append(data[2].strip())

            # 単一の場合
            else:
                # print('No:{} リリース日:{} 判明日:{} Link:{}'.format(number_char, data[1].strip(), data[2].strip(), output_path))
                patient_data_tmp.append(
                    {"No": number_char, "リリース日": data[1].strip(), "link": output_path})
                patients_summary_tmp.append(data[2].strip())

    # convertの実行
    path_op.create_path('text')
    convert_txt = PdfParser()
    convert_txt.executeConvert()

    # テキストからjsonの作成
    parser = TextParser()
    patient_list = []

    # patientの作成
    for tmp in patient_data_tmp:
        result = parser.text2dict(tmp['No'], tmp['link'])
        result.update(tmp)
        result.update({'退院': None})
        del result['link']
        patient_list.append(result)
    patients = {}
    patients['__comments'] = "陽性患者の属性"
    patients['date'] = update_datetime
    # Noに数字が入らない場合の処理（例："再陽性"）
    nan_patient_list = list(filter(lambda x: re.search(
        r'\d', x['No']) is None, patient_list))
    number_patient_list = list(filter(lambda x: re.search(
        r'\d', x['No']) is not None, patient_list))
    insert_patient_list = sorted(number_patient_list, key=lambda x: int(
        re.sub(r'県|内|例|目', '', x['No'])))
    insert_patient_list.extend(nan_patient_list)
    patients['data'] = insert_patient_list
    # patients_summaryの作成
    patients_summary_data = {}
    patients_summary_data['__comments'] = "陽性患者数"
    patients_summary_data['date'] = update_datetime
    patients_summary = TimeUtil().create_dt_dict(datetime.datetime.now())
    for k, g in groupby(patients_summary_tmp):
        patients_summary = list(map(lambda x: {"日付": x["日付"], "小計": len(
            list(g)) if x['日付'] == k else x['小計']}, patients_summary))

    # 小計が0とならない最新の日付までのリストにする
    patients_summary = sorted(patients_summary, key=lambda x: x['日付'])
    jc = JsonChecker()
    patients_summary = jc.exclude_zero_max_date(patients_summary)
    patients_summary_data['data'] = patients_summary

    return patients, patients_summary_data
