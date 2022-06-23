import pymysql


class MySQLConnector:

    def __init__(self, adr, usr, pwd, db):
        self.cur = None
        self.con = None
        self.adr = adr
        self.pwd = pwd
        self.usr = usr
        self.db = db

        self.con = pymysql.connect(host=self.adr, user=self.usr, password=self.pwd, db=self.db)
        self.cur = self.con.cursor()

    def make_a_query(self, query, params=None):
        if params is None:
            self.cur.execute(query)
        else:
            print(query, params)
            self.cur.execute(query, params)
        res = self.cur.fetchall()
        self.con.commit()
        if len(res) == 1:
            return res[0]
        else:
            return res

    def close_connection(self):
        self.con.close()

