# coding: utf-8

import website
import sys, json
from workflow import Workflow

def main(wf):
    website_obj = website.Website()
    if wf.args == None or wf.args == []:
        query = ""
    else:
        query = wf.args[0].strip().replace("\\", "")
    sites = website_obj.query(query)
    for site in sites:
        wf.add_item(title=site["name"], subtitle=site["url"], arg=site["url"], valid=True)
    wf.send_feedback()

if __name__ == "__main__":
    wf = Workflow()
    sys.exit(wf.run(main))
