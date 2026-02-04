# Task 2: Product Inventory
# Build a product inventory system with:

# - Products have: name, price, quantity, category
# - GET endpoint with query parameter to filter products by category
# - GET endpoint to get products within a price range (use two query parameters: min_price, max_price)
# - PUT endpoint to update product quantity only



# imports 
from fastapi import FastAPI, Path, Query
from typing import Optional, List
from pydantic import BaseModel

app = FastAPI()


# data: Products have: name, price, quantity, category
products = {
    1:{
        'name': 'adidas',
        'price': 130,
        'quantity': 10,
        'category': 'shoes'
    },
    2:{
        'name': 'nike',
        'price': 1300,
        'quantity': 15,
        'category': 'shoes'
    },
    3:{
        'name': 'on',
        'price': 100,
        'quantity': 100,
        'category': 'shoes'
    },
    4:{
        'name': 'polo rl',
        'price': 1300,
        'quantity': 20,
        'category': 'shirt'
    }
}

# - GET endpoint with query parameter to filter products by category
@app.get('/products/')
def get_products(category: Optional[str] = Query(default=None)):
    if category:
        filtered_prods =[
            p for p in products.values() if p['category'] == category
        ]
        return filtered_prods
    return products

# - GET endpoint to get products within a price range (use two query parameters: min_price, max_price)
@app.get('/products', response_model=List[dict])
def get_products_by_range(min_price: float = Query(..., ge=0), max_price: float = Query(..., ge=0)):
    return [
        prod for prod in products.values() if min_price<=prod['price']<=max_price
    ]


# - PUT endpoint to update product quantity only

class UpdateProductQuantity(BaseModel):
    quantity: int


@app.put('/products/{product_id}')
def update_product(product_id: int, product: UpdateProductQuantity):
    if product_id not in products:
        return {'Error': 'Product does not exist'}
    
    # Update only the quantity in the dictionary
    products[product_id]['quantity'] = product.quantity
    
    return products[product_id] 