from fastapi import FastAPI
from db_worker import Connect2Database
from project_utils import create_query_for_inserting_form_parser


app = FastAPI()


@app.get('/user_form/{user_form}')
def set_user_form(user_form: dict):
    connector = Connect2Database()
    cursor = connector.get_cursor()
    cursor.execute(create_query_for_inserting_form_parser(user_form))
    connector.commit()

