from fastapi import FastAPI
from datetime import date
from pydantic import BaseModel
from json import JSONEncoder
import json
import uvicorn
from mysql.connector import connect, Error

class Product(BaseModel):
    id: int = None
    name: str
    cost: int

class EmployeeEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__

app = FastAPI()

def serialize(obj):
    return json.dumps(obj, cls=EmployeeEncoder, ensure_ascii=False)
     
@app.get('/')
def home():
    return get_products()

@app.get('/products')
def get_products():
    products = get_products_from_db()
    return serialize(products)

@app.get('/products/{productId}')
def get_product(productId: int): 
    products = get_product_from_db(productId)
    return serialize(products[productId])
    
@app.post('/products')
def create_product(newproduct: Product):
    insert_query = f"INSERT INTO catalog.products(name, cost) VALUES('{newproduct.name}', {newproduct.cost});"
    execute_query(insert_query)

@app.put('/products')
def put_product(newproduct: Product):
    update_query = f"UPDATE catalog.products SET name = '{newproduct.name}', cost = {newproduct.cost} WHERE id = {newproduct.id};"
    execute_query(update_query)
    
@app.delete('/products/{productId}')
def delete_product(productId: int):
    delete_query = f"DELETE FROM catalog.products WHERE id = {productId};"
    execute_query(delete_query)

def get_product_from_db(id: int):
    select_product_query = f"SELECT id, name, cost FROM catalog.products WHERE id = {id};"
    table = execute_select_query(select_product_query)
    row = table[0]
    Myproduct = Product(id = row[0], name = row[1], cost = row[2])
    return Myproduct
    
def get_products_from_db():
    select_products_query = "SELECT id, name, cost FROM catalog.products;"
    table = execute_select_query(select_products_query)
    products = list()
    for row in table:
        Myproduct = Product(id = row[0], name = row[1], cost = row[2])
        products.append(Myproduct)
    return products

def execute_select_query(query: str):
    #try:
        with connect(
        host="localhost",
        user='root',
        password='242338',
        ) as connection:
            with connection.cursor() as cursor:
                cursor.execute(query)
                return cursor.fetchall()
                
def execute_query(query: str):
    #try:
        with connect(
        host="localhost",
        user='root',
        password='242338',
        ) as connection:
            with connection.cursor() as cursor:
                cursor.execute(query)
                connection.commit()

if __name__ == '__main__':
    uvicorn.run('main:app', port=8000, host='0.0.0.0', reload=True)