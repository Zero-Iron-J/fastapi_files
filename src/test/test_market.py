from src.model.market import Market
from src.service import market as code

sample =  Market(name = "치킨마니아", call_num = "088-123-1234", menu = {"fried chicken" : 20000}, location = "서울")

def test_get_exist():
    resp = code.get_market("치킨마니아")
    assert resp == sample

def test_get_missing():
    resp = code.get_market("피자헛")
    assert resp is None