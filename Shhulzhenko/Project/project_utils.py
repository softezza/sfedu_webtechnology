import re


def check_match(val: str):
    """
    Проверка по шаблонам вверно введенные данные для отправки сообщения
    """
    email_template = "\w+@\w+\.\w+"
    num_of_phone_template = "8\d{10}"
    return True if re.fullmatch(email_template, val) or re.fullmatch(num_of_phone_template, val) else False


def generate_key():
    """Генерация одноразового ключа подтверждения и отправка пользователю по указанным данным"""
    return