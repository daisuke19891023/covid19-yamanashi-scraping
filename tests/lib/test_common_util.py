import pytest
from src.lib.common_util import TimeUtil


def test_getWareki():
    tmu = TimeUtil()
    wareki, other = tmu.getWareki('令和2年10月31日')
    assert wareki == '令和'
    #assert other == '2年10月31日'


def test_getWareki_heisei():
    tmu = TimeUtil()
    wareki, other = tmu.getWareki('平成30年1月31日')
    assert wareki == '平成'
    assert other == '30年1月31日'


if __name__ == '__main__':
    pytest.main(['-v', __file__])
