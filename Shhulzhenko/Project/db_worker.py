import pymysql


class Connect2Database:
    def __init__(self):
        print('Инициируем подключение к бд')
        self.connect_to_bd()

    def connect_to_bd(self):
        self._kzsp_conf = pymysql.connect(user='user_',
                                          password='1234qwerty',
                                          database='do_not_know_base')
        self._cursor = self._kzsp_conf.cursor()

    def __del__(self):
        print('удаление экземпляра')
        self._close()

    def get_cursor(self):
        if not self._kzsp_conf.open:
            self.connect_to_bd()
        return self._cursor

    def close_connect(self, initiator):
        print('ручное закрытие подключения к бд', initiator)
        self._close()

    def _close(self):
        if self._kzsp_conf.open:
            self._kzsp_conf.close()
        else:
            print('Подключение уже было закрыто')

    def commit(self):
        if not self._kzsp_conf.open:
            return
        self._kzsp_conf.commit()
