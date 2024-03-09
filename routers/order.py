from fastapi import APIRouter, Depends,status, HTTPException

from schema.order import Order, OrderCreate, orders, CheckoutOrder, Status
from services.order import order_service

order_router = APIRouter()

# list all order
# create an order 

@order_router.get('/', status_code=200)
def list_orders():
    response = []
    response = order_service.order_parser(orders)
    return {'message': 'success', 'data': response}

@order_router.post('/', status_code=201)
def create_order(payload: OrderCreate = Depends(order_service.check_availability)):
    customer_id: int = payload.customer_id
    product_ids: list[int] = payload.items
    # get curr order id
    order_id = len(orders) + 1
    new_order = Order(
        id=order_id,
        customer_id=customer_id,
        items=product_ids,
        status = Status.pending
    )
    orders.append(new_order)
    return {'message': 'Order created successfully', 'data': new_order}

@order_router.put('/{order_id}', status_code=status.HTTP_202_ACCEPTED)
def checkout_order(order_id: int, payload: Status):
    check = None
    for order in orders:
        if order.id == order_id:
            check = order
            break
    if not check:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="The order id does not exist")
    check.status = payload  
    return {"message": "The order has been completed", "data": {"order_id": check.id, "status": check.status}}



