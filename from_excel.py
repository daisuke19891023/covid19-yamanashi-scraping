import os
import pandas as pd
import simplejson as json
import datetime
import requests
import re
from src.data_updater import DataUpdater
from typing import Tuple
from bs4 import BeautifulSoup


def get_excel_url(base_url: str, elem_type: str) -> str:
    r = requests.get(base_url)
    r.encoding = r.apparent_encoding
    soup = BeautifulSoup(r.text, 'html.parser')
    elems = soup.find(href=re.compile(elem_type))
    try:
        return elems.get('href')
    except:
        raise FileNotFoundError(
            f"excel file not found in url: {base_url} \n fale: {elem_type}")


def download_file(url: str, file_name: str, skip_flg=False) -> pd.DataFrame:
    file_bin = requests.get(url)
    with open(file_name, "wb") as file:
        file.write(file_bin.content)
    if skip_flg:
        df = pd.read_excel(file_name, index_col=0,
                           skiprows=1)
    else:
        df = pd.read_excel(file_name)
    return df


# 陽性者の状況
def create_yousei_data(excel_url: str, file_name: str,
                       dt_yesterday: datetime.datetime) \
        -> Tuple[pd.DataFrame, pd.DataFrame]:

    df_yousei = download_file(excel_url, file_name)

    df_yousei.columns = df_yousei.columns.map(lambda s: s.replace("\n", ""))
    df_yousei.rename(columns={"№": "No", "居住地（生活圏）": "居住地"}, inplace=True)

    # 改行除去
    df_yousei["居住地"] = df_yousei["居住地"].str.replace(
        "\n", "").str.normalize("NFKC")
    df_yousei["年代"] = df_yousei["年代"].str.replace("\n", "")

    # 非公表
    df_yousei["年代"] = df_yousei["年代"].fillna("非公表")
    df_yousei["性別"] = df_yousei["性別"].fillna("非公表")

    df_yousei["症状"] = df_yousei["発症日"].where(
        df_yousei["発症日"].isin(["無症状", "非公表"]))
    df_yousei["発症日"] = pd.to_datetime(df_yousei["発症日"], errors="coerce")

    df_yousei["No"] = "県内" + df_yousei["No"].astype(str) + "例目"

    df_yousei["発生判明日"] = df_yousei["公表日"].apply(
        lambda d: pd.Timestamp(d, tz="Asia/Tokyo").isoformat()
    )

    df_yousei["退院"] = None

    df_patients = df_yousei.reindex(
        columns=["年代", "性別",  "居住地", "No", "発生判明日", "退院"])

    # 陽性患者数

    ser_patients_sum = df_yousei["公表日"].value_counts().sort_index()

    if dt_yesterday > ser_patients_sum.index[-1]:
        ser_patients_sum[dt_yesterday] = 0

    ser_patients_sum.sort_index(inplace=True)
    df_patients_sum = pd.DataFrame(
        {"小計": ser_patients_sum.asfreq("D", fill_value=0)})

    df_patients_sum["日付"] = df_patients_sum.index.map(
        lambda d: pd.Timestamp(d, tz="Asia/Tokyo").isoformat()
    )
    df_patients_sum = df_patients_sum.reindex(columns=["日付", "小計"])

    return df_patients, df_patients_sum


# 電話相談件数
def create_soudan_data(excel_url: str, file_name: str,
                       dt_date: datetime.datetime) \
        -> Tuple[pd.DataFrame, pd.DataFrame]:
    df_soudan = download_file(excel_url, file_name, skip_flg=True)

    df_soudan = df_soudan[df_soudan.index < dt_date].fillna(0).astype(int)

    df_soudan["日付"] = df_soudan.index.map(
        lambda d: pd.Timestamp(d, tz="Asia/Tokyo").isoformat()
    )

    df_soudan.head(10)

    df_contacts = (
        df_soudan.loc[:, ["日付", "専用相談ダイヤル相談件数"]]
        .rename(columns={"専用相談ダイヤル相談件数": "小計"})
        .copy()
    )
    df_contacts = df_contacts.reindex(columns=["日付", "小計"])

    df_querents = (
        df_soudan.loc[:, ["日付", "保健所相談件数"]].rename(
            columns={"保健所相談件数": "小計"}).copy()
    )
    df_querents = df_querents.reindex(columns=["日付", "小計"])

    return df_contacts, df_querents


# 衛生環境研究所におけるPCR検査数

def create_pcr_data(excel_url: str, file_name: str,
                    dt_date: datetime.datetime) \
        -> pd.DataFrame:

    df_pcr = download_file(excel_urls[2], files[2], skip_flg=True)

    df_pcr.rename(columns={"検査数": "小計"}, inplace=True)

    df_pcr = df_pcr[df_pcr.index < dt_date].fillna(0).astype(int)

    df_pcr["日付"] = df_pcr.index.map(
        lambda d: pd.Timestamp(d, tz="Asia/Tokyo").isoformat())
    df_pcr = df_pcr.reindex(columns=["日付", "小計"])
    return df_pcr


if __name__ == '__main__':
    # preproccessing
    base = "https://www.pref.yamanashi.jp"
    dt_now = datetime.datetime.now()
    dt_date = dt_now.replace(hour=0, minute=0, second=0, microsecond=0)
    dt_yesterday = dt_date - datetime.timedelta(days=1)
    dt_update = dt_now.strftime("%Y/%m/%d %H:%M")
    data = {}

    base_urls = ["/koucho/coronavirus/info_coronavirus_prevention.html",
                 "/koucho/coronavirus/info_coronavirus_data.html",
                 "/koucho/coronavirus/info_coronavirus_data.html"]
    #  "/koucho/coronavirus/info_coronavirus_data.html"]
    files = ["yousei.xlsx", "soudan.xlsx", "pcr"]
    # , "cva.xlsx"]
    excel_urls = []
    for base_url, elem_type in zip(base_urls, files):
        base_url = base + base_url
        target_url = get_excel_url(base_url, elem_type)
        excel_urls.append(base + target_url)

    # 陽性者の情報取得
    df_patients, df_patients_sum = create_yousei_data(
        excel_urls[0], files[0], dt_yesterday)
    data["patients"] = {
        "__comments": "陽性患者の属性",
        "date": dt_update,
        "data": df_patients.to_dict(orient="records"),
    }

    data["patients_summary"] = {
        "__comments": "陽性患者数",
        "date": dt_update,
        "data": df_patients_sum.to_dict(orient="records"),
    }

    # 電話相談件数
    df_contacts, df_querents = create_soudan_data(
        excel_urls[1], files[1], dt_date)

    data["contacts"] = {
        "__comments": "新型コロナウイルス感染症専用相談ダイヤル相談件数",
        "date": dt_update,
        "data": df_contacts.to_dict(orient="records"),
    }

    data["querents"] = {
        "__comments": "帰国者・接触者相談センター相談件数",
        "date": dt_update,
        "data": df_querents.to_dict(orient="records"),
    }

    # 衛生環境研究所におけるPCR検査数
    df_pcr = create_pcr_data(excel_urls[2], files[2], dt_date)

    data["inspections_summary"] = {
        "__comments": "県内の疑似症例の検査状況",
        "date": dt_update,
        "data": df_pcr.to_dict(orient="records"),
    }
    # 更新日時設定

    data["lastUpdate"] = dt_update

    # update data.json
    du = DataUpdater('data.json')
    du.update_data(data)
    # ファイル削除
    for file in files:
        os.remove(file)
