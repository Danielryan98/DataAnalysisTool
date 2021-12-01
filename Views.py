import json
import re
# import Tkinter as tk
import matplot as mp

class Views:
    def __init__(self, uuid):
        self.uuid = uuid

        self.dataList = []
        for line in open('test_data2.json', 'r'):
            self.dataList.append(json.loads(line))

    def bycountry(self):
        for entry in self.dataList:
            for k, v in entry.items():
                if v == self.uuid:
                    print(v)


    def bycontinent(self):
        print("Views by ... class")

    def bybrowser(self):
        # browserSet = set([])
        # for entry in self.dataList:
        #     browserSet.add(entry["visitor_useragent"])
        # print(browserSet)
        browserDict = {}
        for entry in self.dataList:
            if entry["visitor_useragent"] not in browserDict:
                browserDict.update({entry["visitor_useragent"]: 1})
            else:
                browserDict[entry["visitor_useragent"]] = browserDict[entry["visitor_useragent"]] + 1

        browserNamesDict = {}
        for entry in self.dataList:
            s = re.match("(.*?)/",entry["visitor_useragent"]).group()
            if s not in browserNamesDict:
                browserNamesDict.update({s: 1})
            else:
                browserNamesDict[s] = browserNamesDict[s] + 1
            # if re.match("(.*?)/",entry["visitor_useragent"]).group() not in browserNamesDict:
            #     browserNamesDict.update({re.match("(.*?)/",entry["visitor_useragent"]).group()})
            # else:
            #     browserNamesDict[re.match("(.*?)/",entry["visitor_useragent"]).group()] = browserNamesDict[re.match("(.*?)/",entry["visitor_useragent"]).group()] + 1
            # if entry[s] not in browserNamesDict:
            #     browserNamesDict.update({s: 1})
            # else:
            #     browserNamesDict[entry[s]] = browserNamesDict[entry[s]]
        
        print(browserNamesDict)

view = Views("130505212721-f307a8c599d3460885c910bdb9c36920")
view.bybrowser()
view.bycountry()