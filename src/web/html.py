from fastapi import APIRouter, Body, HTTPException, Request, Form
from model.customer import Customer
from service import customer as service
from error import Missing, Duplicate
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from starlette.responses import RedirectResponse


router = APIRouter(prefix = "/html")

#기본 템플릿 위치를 지정합니다
templates = Jinja2Templates(directory="templates")

@router.get("")
@router.get("/", response_class=HTMLResponse)
def get_all(request : Request):
    customers = service.get_all()
    return templates.TemplateResponse("index.html", 
        {"request" : request, "customers" : customers})


@router.post("/", response_class=HTMLResponse)
def create_customer(request : Request,
    name = Form(...),
    home = Form(...),
    call_num = Form(...),
    email = Form(...)
):
    service.create_customer(Customer(name=name, home=home, call_num=call_num, email=email))
    return RedirectResponse("/html",status_code=302)

@router.post("/update", response_class=HTMLResponse)
def modify_customer(request : Request,
    origin_name = Form(...),
    name = Form(...),
    home = Form(...),
    call_num = Form(...),
    email = Form(...)
    ):
    service.modify_customer(name, Customer(name=name,home=home,call_num=call_num,email=email))
    return RedirectResponse("/html",status_code=302)

@router.post("/delete", response_class=HTMLResponse)
def delete_customer(request : Request,
    name = Form(...)):
    service.delete_customer(name)
    return RedirectResponse("/html",status_code=302)