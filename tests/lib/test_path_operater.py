import pytest
from src.lib.path_operator import PathOperator
import os


@pytest.fixture(scope="module", autouse=True)
def create_dir_object():
    po = PathOperator()
    tmp_folder_name = 'hoge'
    yield po, tmp_folder_name
    if(os.path.exists(tmp_folder_name)):
        os.removedirs(tmp_folder_name)


@pytest.fixture(scope="module", autouse=True)
def exists_dir_object():
    po = PathOperator()
    tmp_folder_name = 'huga'
    os.makedirs(tmp_folder_name)
    yield po, tmp_folder_name
    if(os.path.exists(tmp_folder_name)):
        os.removedirs(tmp_folder_name)


@pytest.fixture(scope="module", autouse=True)
def file_name_object():
    po = PathOperator()
    yield po


class TestPathOperater:
    def test_create_path(self, create_dir_object, capsys):
        create_dir_object[0].create_path(create_dir_object[1])
        captured = capsys.readouterr()
        assert captured.out == f'create path name: {create_dir_object[1]}\n'
        assert os.path.exists(create_dir_object[1]) == True

    def test_create_path_exists(self, exists_dir_object, capsys):
        exists_dir_object[0].create_path(exists_dir_object[1])
        captured = capsys.readouterr()
        assert captured.out == f'path name: {exists_dir_object[1]} already exists\n'

    @pytest.mark.parametrize("test_input, expected", [('/huga/example1.json', 'example1.json'),  ('/example2.txt', 'example2.txt')])
    def test_get_file_name(self, file_name_object, test_input, expected):
        result = file_name_object.get_file_name(test_input)
        assert result == expected

    def test_set_downlaod_file_name(self, file_name_object):
        result = file_name_object.set_downlaod_file_name(
            'huga', 'example1.json')
        assert result == os.path.join(os.getcwd(), 'huga', 'example1.json')
