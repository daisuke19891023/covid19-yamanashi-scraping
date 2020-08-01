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
import bs4


class Patient:
    def __init__(self, update_datetime):

        self.patient_list = []

        self.patients = {}
        self.patients['__comments'] = "陽性患者の属性"
        self.patients['date'] = update_datetime

        self.patients_summary_data = {}
        self.patients_summary_data['__comments'] = "陽性患者数"
        self.patients_summary_data['date'] = update_datetime

    def get_patient_dict(self, source_url, target_url, scr):
        # 発生状況等の取得
        url = scr.getTargetUrl(source_url, target_url)
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
                        # print('No:{} 発生判明日:{} Link:{}'.format(n, data[1].strip(), data[2].strip(), output_path))
                        patient_data_tmp.append(
                            {"No": n, "発生判明日": data[2].strip(), "link": output_path})

                # 単一の場合
                else:
                    # print('No:{} 発生判明日:{} Link:{}'.format(number_char, data[1].strip(), data[2].strip(), output_path))
                    patient_data_tmp.append(
                        {"No": number_char,  "発生判明日": data[2].strip(), "link": output_path})

        # convertの実行
        path_op.create_path('text')
        PdfParser.execute_pdf2text()

        # patientの作成
        for tmp in patient_data_tmp:
            # テキストからjsonの作成
            result = TextParser.text2dict(tmp['No'], tmp['link'])
            result.update(tmp)
            result.update({'退院': None})
            del result['link']
            self.patient_list.append(result)

        # Noに数字が入らない場合の処理（例："再陽性"）
        nan_patient_list = list(filter(lambda x: re.search(
            r'\d', x['No']) is None, self.patient_list))
        number_patient_list = list(filter(lambda x: re.search(
            r'\d', x['No']) is not None, self.patient_list))
        insert_patient_list = sorted(number_patient_list, key=lambda x: int(
            re.sub(r'県|内|例|目|第\d報', '', x['No'])))
        insert_patient_list.extend(nan_patient_list)
        self.patients['data'] = insert_patient_list

        # patients_summaryの作成
        self.create_patients_summary_dict(insert_patient_list)
        return self.patients, self.patients_summary_data

    def create_patients_summary_dict(self, patient_list):
        # patients_summaryの作成
        patients_summary = TimeUtil().create_dt_dict(datetime.datetime.now())
        # patient_listから"発生判明日"のみのリストを作成
        patients_summary_tmp = list(map(lambda x: x["発生判明日"], patient_list))

        for k, g in groupby(patients_summary_tmp):
            patients_summary = list(map(lambda x: {"日付": x["日付"], "小計": len(
                list(g)) if x['日付'] == k else x['小計']}, patients_summary))

        # 小計が0とならない最新の日付までのリストにする
        patients_summary = sorted(patients_summary, key=lambda x: x['日付'])
        patients_summary = JsonChecker.exclude_zero_max_date(patients_summary)
        self.patients_summary_data['data'] = patients_summary

    def sort_patients_dict(self, patients_before: dict) -> dict:
        patients_after = {}
        keys = ("年代", "性別", "居住地", "No", "発生判明日", "退院")
        for key in keys:
            patients_after[key] = patients_before[key]
        return patients_after

    def create_new_patient_dict(self, patient_soup, scr):

        # 対象の階層のデータだけ抽出する
        data = scr.find_h4(patient_soup)
        patients = []
        patient = {}
        patient["No"] = StringUtil.exclude_info_number(data.text)

        for index, sibling in enumerate(data.next_siblings):
            # if index % 2 != 0:  # 改行コードはスキップする
            if hasattr(sibling, "text"):
                target = sibling.text
            else:
                target = sibling

            # h4属性の場合、新たなpatient dictを作成する
            if sibling.name == 'h4':
                patient["退院"] = None
                if patient["発生判明日"] is not None:
                    patient["発生判明日"] = TimeUtil().convert_wareki_to_ad(
                        patient["発生判明日"])
                patients.append(self.sort_patients_dict(patient))
                patient = {}
                patient["No"] = StringUtil.exclude_info_number(target)
                continue

            # 年代|性別|発生判明日|居住地の情報をセットする
            flg, key, value = StringUtil.set_key_value(target)
            if flg and key not in patient:
                patient[key] = value

            # h2タグが表示された時点で別と患者情報の表示は終了する
            if sibling.name == 'h2':
                patient["退院"] = None
                if patient["発生判明日"] is not None:
                    patient["発生判明日"] = TimeUtil().convert_wareki_to_ad(
                        patient["発生判明日"])
                patients.append(self.sort_patients_dict(patient))
                break
        print(patients)
        self.patient_list = list(filter(lambda x: re.search(
            r'\d', x['No']) is not None, patients))
