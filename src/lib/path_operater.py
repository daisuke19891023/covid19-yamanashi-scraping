import os
import shutil


class PathOperater:
    def __init__(self):
        self.current = os.getcwd()

    def createPath(self, path_name):
        target_path = os.path.join(self.current, path_name)
        if(os.path.exists(target_path)):
            return 1
        else:
            os.makedirs(target_path)
            return 0

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
