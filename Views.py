import json
import re
import pycountry_convert as pc
import httpagentparser as hp
from multipledispatch import dispatch

class Views:
    def __init__(self):
        self.dataList = []
        for line in open('sample_100k_lines.json', 'r'):
            self.dataList.append(json.loads(line))

        self.browserDict = {}
        self.browserNamesDict = {}
        self.countriesDict = {}
        self.continentsDict = {}
        self.usersDict = {}
        self.delete_list = []

    # uses the subject_doc_id to uniquely specify a document
    def bycountry(self, docUUID):
        for entry in self.dataList:
            for k, v in entry.items():
                if v == docUUID:
                    if entry["visitor_country"] not in self.countriesDict:
                        self.countriesDict.update({entry["visitor_country"]: 1})
                    else:
                        self.countriesDict[entry["visitor_country"]] = self.countriesDict[entry["visitor_country"]] + 1
        return self.countriesDict

    def bycontinent(self, docUUID):
        for entry in self.dataList:
            for k, v in entry.items():
                if v == docUUID:
                    continent = pc.country_alpha2_to_continent_code(entry["visitor_country"])
                    if continent not in self.continentsDict:
                        self.continentsDict.update({continent: 1})
                    else:
                        self.continentsDict[continent] = self.continentsDict[continent] + 1
        return self.continentsDict

    def bybrowser(self):
        for entry in self.dataList:
            if entry["visitor_useragent"] not in self.browserDict:
                self.browserDict.update({entry["visitor_useragent"]: 1})
            else:
                self.browserDict[entry["visitor_useragent"]] = self.browserDict[entry["visitor_useragent"]] + 1
        print(self.browserDict.values())

        for entry in self.browserDict:
            entry_data = hp.detect(entry)
            if 'browser' in entry_data:
                x = entry_data.get("browser")
                x = x.get('name')
                if x not in self.browserNamesDict:
                    self.browserNamesDict.update({x: 1})
                else:
                    self.browserNamesDict[x] = self.browserNamesDict[x] + 1
        self.browserNamesDict["Other"] = 0
        for browser, count in self.browserNamesDict.items():
            if count < 50:
                self.browserNamesDict["Other"] += count
                self.delete_list.append(browser)
        for browser in self.delete_list:
            del self.browserNamesDict[browser]
        return self.browserNamesDict

    def userMinutes(self):
        for entry in self.dataList:
            # not all entries have even_readtime key so first check for it here
            if "event_readtime" in entry:
                # then can add the user to the users dict if they don't already exist with time as a key
                if entry["visitor_uuid"] not in self.usersDict:
                    self.usersDict.update({entry["visitor_uuid"]: entry["event_readtime"]})
                else:
                    # if the user exists already then update the time value
                    self.usersDict[entry["visitor_uuid"]] += entry["event_readtime"]
        # then sort the dict by time value in descending order
        self.usersDict = (dict(sorted(self.usersDict.items(), key=lambda item: item[1], reverse=True)))
        return self.usersDict

    def readersOfDoc(self, docUUID):
        userUUIDs = []
        for entry in self.dataList:
            if entry["event_type"] == "read":
                if entry["subject_doc_id"] == docUUID:
                    userUUIDs.append(entry["visitor_uuid"])
        return userUUIDs

    def docsReadByVisitor(self, visUUID):
        docUUIDs = []
        for entry in self.dataList:
            if entry["event_type"] == "read":
                 if entry["visitor_uuid"] == visUUID:
                    docUUIDs.append(entry["subject_doc_id"])
        return docUUIDs

    def sortFunc(self, x, dict):
        n = 0
        for k in dict.keys():
            if x in dict[k]:
                n += 1
        return n

    @dispatch(object, object)
    def alsoLikes(self, docUUID, sortFunc):
        alsoLikesDict = {}
        userUUIDS = self.readersOfDoc(docUUID)
        for user in userUUIDS:
            alsoLikesDict.update({user: self.docsReadByVisitor(user)})
        
        xs = set([])
        for k in alsoLikesDict.keys():
            xs = xs | set(alsoLikesDict[k])
        xs_sort = [(sortFunc(x,alsoLikesDict), x) for x in xs]

        xs_sort.sort()

        return xs_sort

    @dispatch(object, object, object)
    def alsoLikes(self, docUUID, userUUID, sortFunc):
        alsoLikesDict = {}
        userUUIDS = self.readersOfDoc(docUUID)
        for user in userUUIDS:
            if user == userUUID:
                alsoLikesDict.update({userUUID: docUUID})
            else:
                alsoLikesDict.update({user: self.docsReadByVisitor(user)})
        
        xs = set([])
        for k in alsoLikesDict.keys():
            xs = xs | set(alsoLikesDict[k])
        xs_sort = [(sortFunc(x,alsoLikesDict), x) for x in xs]

        xs_sort.sort()

        return xs_sort





    

view = Views()
# view.bybrowser()
# print(view.bycountry("080826024732-2c61742d5b4743f88576f5c97457b12a"))
# print(view.bycontinent("080826024732-2c61742d5b4743f88576f5c97457b12a"))
# view.userMinutes()
# print(view.readersOfDoc("140310170010-0000000067dc80801f1df696ae52862b"))
# print(view.docsReadByVisitor("4065369dbee2b902"))
# print(view.alsoLikes("140310170010-0000000067dc80801f1df696ae52862b", view.sortFunc))
# print(view.alsoLikes("140310170010-0000000067dc80801f1df696ae52862b", "53a376a3e4caa372", view.sortFunc))

print(view.alsoLikes("100806162735-00000000115598650cb8b514246272b5", view.sortFunc))
print(view.alsoLikes("100806162735-00000000115598650cb8b514246272b5", "00000000deadbeef", view.sortFunc))

