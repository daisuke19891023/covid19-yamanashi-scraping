import datetime
import os
import re
import shutil


class StringUtil:
    def __init__(self):
        super().__init__()
        self.exclude_char = r'県外'

    def exclude_outside(self, full_with_str):
        if re.search(self.exclude_char, full_with_str):
            return False
        else:
            return True

    def is_duplicate_data(self, number_char):
        check = re.search(r',', number_char)
        if check is None:
            return False, number_char
        else:
            tmp = re.sub(r'県|内|例|目', '', number_char)
            return True, list(map(lambda x: '県内{}例目'.format(x), tmp.split(',')))


class PathOperater:
    def __init__(self):
        self.current = os.getcwd()

    def createPath(self, path_name):
        target_path = os.path.join(self.current, path_name)
        if(os.path.exists(target_path)):
            return 0
        else:
            os.makedirs(target_path)

    def getFileName(self, url_file_path):
        return os.path.basename(url_file_path)

    def setDownlaodFileName(self, path, fileName):
        return os.path.join(self.current, path, fileName)

    def removePath(self, path_name):
        target_path = os.path.join(self.current, path_name)
        if(os.path.exists(target_path)):
            shutil.rmtree(target_path)
        else:
            return 0


if __name__ == '__main__':
    result, char = StringUtil().is_duplicate_data("県内10,11例目")
    print(char)
