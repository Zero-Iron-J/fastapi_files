from src.model.customer import Customer
from src.data import customer as code

sample = Customer(
    name = "jane",
    call_num="010-1234-5678", 
    home="강원도 춘천", 
    email="jane123@naver.com"
)

def test_get_exist():
    resp = code.get_customer("jane")
    assert resp == sample

def test_get_missing():
    resp = code.get_customer("lily")
    assert resp is None