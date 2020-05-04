from src.lib.json_checker import JsonChecker


def getStaticsDataDict(scr, table, comments, update_datetime):
    res_dict = scr.parseContactsTable(table)

    # jsonへの格納
    dictonary = {}
    dictonary['__comments'] = comments
    dictonary['date'] = update_datetime

    # 小計が0とならない最新の日付までのリストにする
    jc = JsonChecker()
    data = sorted(res_dict, key=lambda x: x['日付'])
    data = jc.exclude_zero_max_date(data)
    dictonary['data'] = data

    return dictonary
