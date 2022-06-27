from fastapi import FastAPI
from datetime import date
from pydantic import BaseModel
from json import JSONEncoder
import json
import uvicorn
from mysql.connector import connect, Error

class Products(BaseModel):
    id: int = None
    id_list: int
    name: str
    weight: str
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
    products = get_lists_from_db()
    return serialize(products)

@app.get('/products/{productsId}')
def get_products(productsId: int): 
    products = get_products_from_db(productsId)
    return serialize(products[productsId])

@app.post('/products')
def create_products(newproducts: Products):
    insert_query = f"INSERT INTO catalog.products(name, weight, cost) VALUES('{newproducts.name}', '{newproducts.weight}', {newproducts.cost});"
    execute_query(insert_query)

@app.put('/products')
def put_product(newproduct: Products):
    update_query = f"UPDATE catalog.products SET name = '{newproducts.name}', weight = '{newproducts.weight}', cost = {newproducts.cost} WHERE id = {newproducts.id};"
    execute_query(update_query)
    
@app.delete('/products/{productsId}')
def delete_products(productsId: int):
    delete_query = f"DELETE FROM catalog.products WHERE id = {productsId};"
    execute_query(delete_query)

def get_products_from_db(id: int):
    select_product_query = f"SELECT id, name, weight, cost FROM catalog.products WHERE id = {id};"
    table = execute_select_query(select_products_query)
    row = table[0]
    Myproducts = Products(id = row[0], name = row[1], weight = row [2], cost = row[3])
    return Myproducts
    
def get_products_from_db():
    select_products_query = "SELECT id, name, weight, cost FROM catalog.products;"
    table = execute_select_query(select_products_query)
    products = list()
    for row in table:
        Myproducts = Products(id = row[0], name = row[1], weight = row [2], cost = row[3])
        products.append(Myproducts)
    return products

def execute_select_query(query: str):
    #try:
        with connect(
        host="localhost",
        user='root',
        password='qwerty123',
        ) as connection:
            with connection.cursor() as cursor:
                cursor.execute(query)
                return cursor.fetchall()
                
def execute_query(query: str):
    #try:
        with connect(
        host="localhost",
        user='root',
        password='qwerty123',
        ) as connection:
            with connection.cursor() as cursor:
                cursor.execute(query)
                connection.commit()

if __name__ == '__main__':
    uvicorn.run('main:app', port=8000, host='0.0.0.0', reload=True)