# -*- coding: utf-8 -*-

import sys,sqlite3
from workflow import Workflow

class Website:
    def __init__(self, id, name, url):
        self.id = id
        self.name = name
        self.url = url
    def __eq__(self, other):
        if isinstance(other, Website):
            return ((self.id == other.id) or (self.url == other.url))
        else:
            return False

    def __ne__(self, other):
        return (not self.__eq__(other))

    def __hash__(self):
        return hash(self.id) + hash(self.url)


class Connection:
    def __init__(self, timeout=10):
        self._con = sqlite3.connect('data.db', timeout=timeout)
        self._create_table()
        self.insert('百度', 'http://www.baidu.com')
        self.insert('淘宝', 'http://www.taobao.com')
        self.insert('支付宝', 'http://www.alipay.com')

    def search(self, query):
        sql1 = "select * from website where name like '%" + query +"%';"
        sql2 = "select * from website where url like '%" + query +"%';"
        return self._cursor_to_set(self._con.execute(sql1)) | self._cursor_to_set(self._con.execute(sql2))
    
    def insert(self, name, url):
        sql = "insert into website(name, url) values(\'" + name + "','" + url + "\');"
        return self._con.execute(sql).rowcount
    
    def delete(self, url):
        sql = "delete from website where url = \'" + url + "\';"
        self._con.execute(sql)

    def _cursor_to_set(self, cursor):
        s = set()
        for each in cursor:
            s.add(Website(each[0], each[1], each[2]))
        return s
    
    def _create_table(self):
        self._con.execute('''
                CREATE TABLE if not exists website(
                id INTEGER PRIMARY KEY, 
                name VARCHAR(25),
                url VARCHAR(500) NOT NULL UNIQUE);
                ''')
    
    def destroy(self):
        self._con.close()

def main(wf):
    con = Connection()
    if wf.args == None or wf.args == []:
        query = ""
    else:
        query = wf.args[0].strip().replace("\\", "")
    res_set = con.search(query)
    for item in res_set:
        wf.add_item(title=item.name, subtitle=item.url, arg=item.url, valid=True)
    con.destroy()
    wf.send_feedback()


if __name__ == '__main__':
    wf = Workflow()
    sys.exit(wf.run(main))

