from fastapi import APIRouter, HTTPException, Depends

from schema.customer import Customer, CustomerCreate, customers

customer_router = APIRouter()

# Create customer 
# List customer
# edit customer

def unique_user(username: str):
    for customer in customers:
        if customer.username == username:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already exists")
    return username


# create customer
@customer_router.post('/', status_code=201)
def create_customer(payload: CustomerCreate, username: str = Depends(unique_user)):
    customer_id = len(customers) + 1
    new_customer = Customer(
        id=customer_id, 
        username=payload.username, 
        address=payload.address
    )
    customers.append(new_customer)
    return {'message': 'customer created successfully', 'data': new_customer}

@customer_router.get('/', status_code=200)
def list_customers():
    return {'message': 'success', 'data': customers}

@customer_router.put('/{customer_id}', status_code=200)
def edit_customer(customer_id: int, payload: CustomerCreate):
    curr_customer = None
    # get the customer
    for customer in customers:
        if customer.id == customer_id:
            curr_customer = customer
            break

    if not curr_customer:
        raise HTTPException(status_code=404, detail="customer not found")
    curr_customer.username = payload.username
    curr_customer.address = payload.address
    return {'message': 'customer edited successfully', 'data': curr_customer}
