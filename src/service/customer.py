from data import customer as customer
from model.customer import Customer

def get_all() -> list[Customer]:
    return customer.get_all()

def get_customer(customer_name : str) -> Customer | None:
    return customer.get_customer(customer_name)

def create_customer(new_customer : Customer) -> Customer | None:
    return customer.create_customer(new_customer)

def modify_customer(customer_name : str, modi_customer : Customer) -> Customer:
    return customer.modify_customer(customer_name, modi_customer)

def delete_customer(customer_name : str) -> None:
    return customer.delete_customer(customer_name)