
import json


class JsonChecker:
    def __init__(self):
        pass

    def read_json(self, path):
        f = open(path, encoding='utf-8')
        data = json.load(f)
        return data

    def exclude_date_key(self, obj):
        return_obj = {}
        for key in obj.keys():
            print(key)
            if key != 'lastUpdate' and key != 'date':
                if isinstance(obj[key], dict):
                    tmp = self.exclude_date_key(obj[key])
                else:
                    tmp = obj[key]
                return_obj[key] = tmp
        return return_obj
