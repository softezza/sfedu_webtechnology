import uvicorn
from project_utils import *
from fastapi import FastAPI


app = FastAPI()


@app.post('/sign_in/{val}')
def set_number_of_phone_or_email(val: str):
    if not check_match(val):
        return {"error_value": 'неверный формат'}
    else:
        send_key(val)
        return {'is_ok': 'ожидайте, код подтверждения прийдет в течении 2-х минут'}


if __name__ == "__main__":
    uvicorn.run('sign_in:app',
                port=10000,
                host='127.0.0.1',
                reload=True)
