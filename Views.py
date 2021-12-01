import json
import re
# import Tkinter as tk
import matplot as mp

class Views:
    def __init__(self):
        self.dataList = []
        for line in open('test_data2.json', 'r'):
            self.dataList.append(json.loads(line))

        self.browserDict = {}
        self.browserNamesDict = {}

    def bycountry(self, uuid):
        for entry in self.dataList:
            for k, v in entry.items():
                if v == uuid:
                    print(v)


    def bycontinent(self):
        print("Views by ... class")

    def bybrowser(self):
        for entry in self.dataList:
            if entry["visitor_useragent"] not in self.browserDict:
                self.browserDict.update({entry["visitor_useragent"]: 1})
            else:
                self.browserDict[entry["visitor_useragent"]] = self.browserDict[entry["visitor_useragent"]] + 1

        for entry in self.dataList:
            s = re.match("(.*?)/",entry["visitor_useragent"]).group()
            if s not in self.browserNamesDict:
                self.browserNamesDict.update({s: 1})
            else:
                self.browserNamesDict[s] = self.browserNamesDict[s] + 1
        
        print(self.browserNamesDict)

view = Views()
view.bybrowser()
view.bycountry("140222143932-91796b01f94327ee809bd759fd0f6c76")