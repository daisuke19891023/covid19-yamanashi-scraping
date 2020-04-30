import pytest
from src.lib.path_operater import PathOperater
import os


@pytest.fixture(scope="module", autouse=True)
def create_dir_object():
    po = PathOperater()
    tmp_folder_name = 'hoge'
    yield po, tmp_folder_name
    if(os.path.exists(tmp_folder_name)):
        os.removedirs(tmp_folder_name)


@pytest.fixture(scope="module", autouse=True)
def exists_dir_object():
    po = PathOperater()
    tmp_folder_name = 'huga'
    os.makedirs(tmp_folder_name)
    yield po, tmp_folder_name
    if(os.path.exists(tmp_folder_name)):
        os.removedirs(tmp_folder_name)


@pytest.fixture(scope="module", autouse=True)
def file_name_object():
    po = PathOperater()
    yield po


class TestPathOperater:
    def test_createPath(self, create_dir_object):
        result = create_dir_object[0].createPath(create_dir_object[1])
        assert result == 0
        assert os.path.exists(create_dir_object[1]) == True

    def test_createPath_exists(self, exists_dir_object):
        result = exists_dir_object[0].createPath(exists_dir_object[1])
        assert result == 1

    @pytest.mark.parametrize("test_input, expected", [('/huga/example1.json', 'example1.json'),  ('c:\test\example2.txt', 'example2.txt')])
    def test_getFileName(self, file_name_object, test_input, expected):
        result = file_name_object.getFileName(test_input)
        assert result == expected

    def test_setDownlaodFileName(self, file_name_object):
        result = file_name_object.setDownlaodFileName('huga', 'example1.json')
        assert result == os.path.join(os.getcwd(), 'huga', 'example1.json')

