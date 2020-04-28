from scraping import Scraper, PathOperater
from pdf2text import Pdf2Text
from parserPdf import ParserPdf
import glob
import json
import os
from common_util import StringUtil
if __name__ == '__main__':
    base = "https://www.pref.yamanashi.jp"
    index_html= "/koucho/coronavirus/info_coronavirus.html"
    scr = Scraper(base)
    # 発生状況等の取得
    url2 = scr.getTargetUrl(index_html, 'info_coronavirus_prevention.html')
    print(url2)
    soup2 = scr.getContent(url2)
    #テーブル情報を取得する
    dataset = scr.parseTable(soup2)

    #pdf格納folderの作成
    pathOp = PathOperater()
    pathOp.createPath('pdf')
    #県外事例は除外
    inside_checker = StringUtil()
    tmp_data= []
    for data in dataset:
        if inside_checker.exclude_outside(data[0]):

            # 格納先のファイル名を作成
            file_name = pathOp.setDownlaodFileName('pdf', pathOp.getFileName(data[2]))
            scr.downloadPdf(data[2], file_name)
            output_file = os.path.splitext(os.path.basename(file_name))[0]
            output_path = os.path.join('./text', output_file + '.txt')
            print('No:{} Day:{} Link:{}'.format(data[0], data[1].strip(),output_path))
            tmp_data.append({"No":data[0], "リリース日":data[1].strip(), "link": output_path})
    text_tmp = json.dumps(tmp_data,indent=4,ensure_ascii=False)
    with open('./data_tmp.json', "wb") as f:
        f.write(text_tmp.encode('utf-8', "ignore"))    
    #convertの実行
    convert_txt = Pdf2Text()
    convert_txt.execute()

    #テキストからjsonの作成
    parser = ParserPdf()
    json_list = []
    # for path in glob.glob('./text/*'):
    #     result = parser.text2dict(path)
    #     json_list.append(result)
    for tmp in tmp_data:
        result = parser.text2dict(tmp['link'])
        result.update(tmp)
        del result['link']
        json_list.append(result)
    patients = {}
    patients['data'] = json_list
    patients['__comments'] = "陽性患者の属性"
    result_json = {}
    result_json['patient'] = patients
    #jsonファイルへの書き出し
    text = json.dumps(result_json,indent=4,ensure_ascii=False)
    with open('./data.json', "wb") as f:
        f.write(text.encode('utf-8', "ignore"))

