from scraping import Scraper, PathOperater
from pdf2text import Pdf2Text
from parserPdf import ParserPdf
import glob
import json
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
    for data in dataset:
        print('No:{} Day:{} Link:{}'.format(data[0], data[1].strip(),data[2]))
        # 格納先のファイル名を作成
        file_name = pathOp.setDownlaodFileName('pdf', pathOp.getFileName(data[2]))
        scr.downloadPdf(data[2], file_name)
    
    #convertの実行
    convert_txt = Pdf2Text()
    convert_txt.execute()

    #テキストからjsonの作成
    parser = ParserPdf()
    json_list = []
    for path in glob.glob('./text/*'):
        result = parser.text2dict(path)
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

