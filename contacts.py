from scraping import Scraper
import json
if __name__ == '__main__':
    base = "https://www.pref.yamanashi.jp"
    index_html= "/koucho/coronavirus/info_coronavirus.html"
    scr = Scraper(base)
    # 発生状況等の取得
    url = scr.getTargetUrl(index_html, 'info_coronavirus_data.html')
    soup = scr.getContent(url)
    tables = scr.findAllTable(soup)
    contacts_table = tables[3]
    res_dict = scr.parseContactsTable(contacts_table)

    #jsonへの格納
    contacts = {}
    contacts['__comments'] = "新型コロナウイルス感染症専用相談ダイヤル相談件数"
    contacts['data'] = sorted(res_dict, key=lambda x:x['日付'])

    #jsonファイルへの書き出し
    result_json = {}
    result_json['contacts'] = contacts
    text = json.dumps(result_json,indent=4,ensure_ascii=False)
    with open('./data_contacts.json', "wb") as f:
        f.write(text.encode('utf-8', "ignore"))