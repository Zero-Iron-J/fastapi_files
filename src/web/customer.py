from fastapi import APIRouter, Body, HTTPException
from model.customer import Customer
import service.customer as customer
from error import Missing, Duplicate


router = APIRouter(prefix = "/customer")

@router.get("")
@router.get("/")
def get_all() -> list[Customer]:
    return customer.get_all()

# 고객의 이름을 잘못적었다. => 조회가 되지 않았다. => 고객이 없으면 None을 반환한다.
@router.get("/{customer_name}")
def get_customer(customer_name : str) -> Customer | None:
    try:
        return customer.get_customer(customer_name)
    except Missing as E:
        raise HTTPException(status_code=404, detail=E.msg)

@router.post("")
@router.post("/")
def create_customer(new_customer : Customer = Body(...)) -> Customer:
    try:
        return customer.create_customer(new_customer)
    except Duplicate as E:
        raise HTTPException(status_code=404, detail=E.msg)

@router.put("/{customer_name}")
def modify_customer(customer_name : str, modi_customer :Customer = Body(...)) -> Customer:
    try:
        return customer.modify_customer(customer_name, modi_customer)
    except Missing as E:
        raise HTTPException(status_code=404, detail=E.msg)

@router.delete("/{customer_name}")
def delete_customer(customer_name : str) -> None:
    try:
        return customer.delete_customer(customer_name)
    except Missing as E:
        raise HTTPException(status_code=404, detail=E.msg)