import json

from src.lib.json_checker import JsonChecker


def create_data(new_obj):
    if(check_data(new_obj)):
        text = json.dumps(new_obj, indent=4, ensure_ascii=False)
        with open('./data.json', "wb") as f:
            f.write(text.encode('utf-8', "ignore"))
        print('create new data')
    else:
        print('not updated')


def check_data(new_obj):
    jc = JsonChecker()
    old_obj = jc.read_json('data.json')
    if not jc.check_list_count(old_obj, new_obj, 'patients'):
        return True
    target_props = ('contacts', 'querents', 'inspections_summary')
    for prop in target_props:
        if not jc.check_nonzero_max(old_obj, new_obj, prop):
            return True
    return False
