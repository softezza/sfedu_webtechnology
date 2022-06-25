import re
from db_worker import Connect2Database


key_users = ['login', 'pwd_h', 'reserve']


def check_match(val: str):
    """
    Проверка по шаблонам вверно введенные данные для отправки сообщения
    """
    email_template = "\w+@\w+\.\w+"
    num_of_phone_template = "8\d{10}"
    return re.fullmatch(email_template, val) or re.fullmatch(num_of_phone_template, val)


def send_key(address):
    key = generate_key()
    print('Send {} to {}'.format(key, address))


def generate_key():
    """Генерация одноразового ключа подтверждения и отправка пользователю по указанным данным"""
    return 1111


def is_excist_log(login):
    connector = Connect2Database()
    cursor = connector.get_cursor()
    query = 'SELECT * from users_ where login={}'.format(login)
    return True, tuple2dict(key_users, cursor.fetchone()) if cursor.execute(query=query) else False, None


def is_comparing_passwords(pwd, inform):
    return hashing(pwd) == inform.get('pwd_h')


def tuple2dict(inform, keys_data):
    dict_information = {keys_data[i]: inform[i] for i in range(len(keys_data))}
    return dict_information


def hashing(pwd):
    pwd_h = pwd
    return pwd_h


def create_query_for_inserting_form_parser(data_to_insert):
    query = 'INSERT ALL {}'.format(data_to_insert)
    return query
