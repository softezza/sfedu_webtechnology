from fastapi import FastAPI
from datetime import date
from pydantic import BaseModel
from json import JSONEncoder
import json
import uvicorn
from mysql.connector import connect, Error

class Task(BaseModel):
    id: int = None
    id_list: int
    name: str
    is_completed: bool = False

class MyList(BaseModel):
    id: int = None
    name: str
    tasks: list = None

class EmployeeEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__

app = FastAPI()

def serialize(obj):
    return json.dumps(obj, cls=EmployeeEncoder, ensure_ascii=False)
    #return obj.__dict__
     
@app.get('/')
def home():
    return get_lists()

@app.get('/lists')
def get_lists():
    lists = get_lists_from_db()
    return serialize(lists)

@app.get('/lists/{listId}')
def get_list(listId: int): 
    lists = get_list_from_db(listId)
    return serialize(lists[listId])

@app.get('/tasks')
def get_tasks():
    tasks = get_tasks_from_db()
    return serialize(tasks)

@app.get('/tasks/{taskId}')
def get_task(taskId: int):
    task = get_task_from_db(taskId)
    return serialize(task)
    
@app.post('/lists')
def create_list(newList: MyList):
    insert_query = f"INSERT INTO tasks.list(name) VALUES('{newList.name}');"
    execute_query(insert_query)
    
@app.post('/tasks')
def create_task(newTask: Task):
    insert_query = f"INSERT INTO tasks.task(id_list, name, is_completed) VALUES({newTask.id_list}, '{newTask.name}', False);"
    execute_query(insert_query)

@app.put('/lists')
def put_list(newList: MyList):
    insert_query = f"UPDATE tasks.list SET name = '{newList.name}' WHERE id = {newList.id};"
    execute_query(insert_query)
    
@app.put('/tasks/{taskId}')
def put_task(task: Task):
    insert_query = f"UPDATE tasks.task SET name = '{task.name}', is_completed = {task.is_completed} WHERE id = {task.id};"
    execute_query(insert_query)
    
@app.delete('/lists/{listId}')
def delete_list(listId: int):
    insert_query = f"DELETE FROM tasks.list WHERE id = {listId};"
    execute_query(insert_query)
    
@app.delete('/tasks/{taskId}')
def delete_task(taskId: int):
    insert_query = f"DELETE FROM tasks.task WHERE id = {taskId};"
    execute_query(insert_query)


def get_list_from_db(id: int):
    select_list_query = f"SELECT id, name FROM tasks.list WHERE id = {id};"
    table = execute_select_query(select_list_query)
    row = table[0]
    tasks = get_tasks_by_id_list_from_db(row[0])
    myList = MyList(id = row[0], name = row[1], tasks = tasks)
    return myList
    
def get_lists_from_db():
    select_lists_query = "SELECT id, name FROM tasks.list;"
    table = execute_select_query(select_lists_query)
    lists = list()
    for row in table:
        tasks = get_tasks_by_id_list_from_db(row[0])
        myList = MyList(id = row[0], name = row[1], tasks = tasks)
        lists.append(myList)
    return lists

def get_task_from_db(id: int):
    select_tasks_query = f"SELECT id, id_list, name, is_completed FROM tasks.task WHERE id = {id};"
    table = execute_select_query(select_tasks_query)
    task = Task(id = row[0], id_list = row[1], name = row[2], is_completed = row[3])
    return task

def get_tasks_from_db():    
    select_tasks_query = "SELECT id, id_list, name, is_completed FROM tasks.task;"
    table = execute_select_query(select_tasks_query)
    tasks = list()
    for row in table:
        task = Task(id = row[0], id_list = row[1], name = row[2], is_completed = row[3])
        tasks.append(task)
    return tasks
    
def get_tasks_by_id_list_from_db(id_list: int):    
    select_tasks_query = f"SELECT id, id_list, name, is_completed FROM tasks.task WHERE id_list = {id_list};"
    table = execute_select_query(select_tasks_query)
    tasks = list()
    for row in table:
        task = Task(id = row[0], id_list = row[1], name = row[2], is_completed = row[3])
        tasks.append(task)
    return tasks

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
    #except Error as e:
    #    print(e)
        
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
    #except Error as e:
    #    print(e)

if __name__ == '__main__':
    uvicorn.run('main:app', port=8000, host='0.0.0.0', reload=True)