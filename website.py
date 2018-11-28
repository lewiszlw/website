# coding: utf-8

import os

# 字段分割符
SEPARATOR = "|"
# 存储文件
STORE_FILE = "data.txt"
# 文件注释符
COMMENT_FLAG = "//"

class Website:
    def __init__(self):
        self._create_db_if_not_exists()
        self._lines, self._sites = self._read_lines_and_parse_sites()
        self._file = open(STORE_FILE, "a")

    def __del__(self):
        self._file.close()

    def _read_lines_and_parse_sites(self):
        _file = open(STORE_FILE, "r")
        lines = [ line.decode("utf-8") for line in _file.readlines() if not line.startswith(COMMENT_FLAG)]
        sites = [ dict(name=line.split(SEPARATOR)[0].strip(), url=line.strip("\n").split(SEPARATOR)[1].strip()) for line in lines if line != "\n"]
        _file.close()
        return lines, sites

    def _create_db_if_not_exists(self):
        if not os.path.exists(STORE_FILE):
            open(STORE_FILE, "w").close()

    def query(self, query):
        if query == "":
            return self._sites
        else:
            result_lines = [ line for line in self._lines if query in line]
            return [dict(name=line.split(SEPARATOR)[0].strip(), url=line.strip("\n").split(SEPARATOR)[1].strip()) for line in result_lines]
