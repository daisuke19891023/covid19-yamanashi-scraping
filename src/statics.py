def getStaticsDataDict(scr, table, comments, update_datetime):
    res_dict = scr.parseContactsTable(table)

    # jsonへの格納
    dictonary = {}
    dictonary['__comments'] = comments
    dictonary['date'] = update_datetime
    dictonary['data'] = sorted(res_dict, key=lambda x: x['日付'])
    return dictonary
