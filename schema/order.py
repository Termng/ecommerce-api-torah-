from typing import Union
from pydantic import BaseModel
from schema.customer import Customer
from enum import Enum

from schema.product import Product

class Status(str, Enum):
    pending = 'Pending'
    completed = 'Completed'
      
class Order(BaseModel):
    id: int
    customer_id: Union[int, Customer]
    items: list[int]
    status: Status = Status.pending

class OrderCreate(BaseModel):
    customer_id: int
    items: list[int]
    status: Status = Status.pending

class CheckoutOrder(BaseModel):
    status: Status 


orders = [
    Order(id=1, customer_id=1, items=[1, 2, 3], status = Status.pending)
]