import json
import os
from src.lib.json_checker import JsonChecker


class DataUpdater:
    def __init__(self, target_file):
        self.target_file = target_file

    def update_data(self, new_obj: dict) -> None:
        if(os.path.exists(self.target_file)):
            if(self.check_data(new_obj)):
                print('create new data')
                self.create_data(new_obj)
            else:
                print('not updated')
        else:
            print('create new data')
            self.create_data(new_obj)

    def create_data(self, new_obj: dict) -> None:
        text = json.dumps(new_obj, indent=4, ensure_ascii=False)
        with open(self.target_file, "wb") as f:
            f.write(text.encode('utf-8', "ignore"))

    def check_data(self, new_obj: dict) -> bool:
        old_obj = JsonChecker.read_json(self.target_file)
        if not JsonChecker.check_list_count(old_obj, new_obj, 'patients'):
            return True
        target_props = ('contacts', 'querents', 'inspections_summary')
        for prop in target_props:
            if not JsonChecker.check_nonzero_max(old_obj, new_obj, prop):
                return True
        return False
