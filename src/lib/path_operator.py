import os
import shutil


class PathOperator:
    def __init__(self):
        self.current = os.getcwd()

    def create_path(self, path_name: str) -> None:
        target_path = os.path.join(self.current, path_name)
        if os.path.exists(target_path):
            print('path name: {} already exists'.format(path_name))
        else:
            os.makedirs(target_path)
            print('create path name: {}'.format(path_name))

    def get_file_name(self, url_file_path: str) -> str:
        return os.path.basename(url_file_path)

    def set_downlaod_file_name(self, dir: str, file_name: str) -> str:
        return os.path.join(self.current, dir, file_name)

    def remove_path(self, path_name: str) -> None:
        target_path = os.path.join(self.current, path_name)
        if(os.path.exists(target_path)):
            shutil.rmtree(target_path)
