from src.scraping import Scraper

def getStaticsDataDict(scr, table, comments):
    contacts_table = table
    res_dict = scr.parseContactsTable(contacts_table)

    #jsonへの格納
    contacts = {}
    contacts['__comments'] = comments
    contacts['data'] = sorted(res_dict, key=lambda x:x['日付'])
    return contacts