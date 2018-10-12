# -*- coding: utf-8 -*-

import sys
from website import Connection
from workflow import Workflow

def main(wf):
    con = Connection()
    if wf.args == None or wf.args == []:
        query = ""
        wf.add_item(title="please input website infomation...", valid=True)
    else:
        query = wf.args[0].strip().replace("\\", "")
        query_str = query.encode("utf-8")
        import pdb;pdb.set_trace()
        args = query_str.split(",")
        if len(args) == 2:
            res = con.insert(args[0], args[1])
            if res > 0:
                wf.add_item(title="insert success!!!", valid=True)
            else:
                wf.add_item(title="insert fail!!!", valid=True)
        else:
            wf.add_item(title="website infomation invalid!!!", valid=True)
    con.destroy()
    wf.send_feedback()

if __name__ == "__main__":
    wf = Workflow()
    sys.exit(wf.run(main))
