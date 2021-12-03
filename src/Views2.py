import json
import re
import pycountry_convert as pc
import httpagentparser as hp
from multipledispatch import dispatch

class Views2:
    def __init__(self):
        self.dataList = []
        self.filename = ""
        self.browserDict = {}
        self.browserNamesDict = {}
        self.countriesDict = {}
        self.continentsDict = {}
        self.usersDict = {}
        self.delete_list = []

    def set_file_name(self, filename):
        self.file_name = filename
        for line in open(self.file_name, 'r'):
            self.dataList.append(json.loads(line))

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

    #Needs refactored
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
            if entry["event_type"] == "read" and entry["subject_doc_id"] == docUUID:
                userUUIDs.append(entry["visitor_uuid"])
        return userUUIDs

    def docsReadByVisitor(self, visUUID):
        # a user can read the same document multiple times (as is the case for the doc_uuid and user_uuid used for the 2nd 100k lines test)
        # so make a set to get rid of duplicates
        docUUIDs = []
        for entry in self.dataList:
            if entry["event_type"] == "read" and entry["visitor_uuid"] == visUUID:
                if entry["subject_doc_id"] not in docUUIDs:
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
        
        # xs is the set of all read document UUIDs, and because its a set it gets rid of duplicates
        xs = set([])
        for k in alsoLikesDict.keys():
            # gets the list of document UUIDs associated with a key k and adds them to the set xs
            xs = xs | set(alsoLikesDict[k])
        xs_sort = [[sortFunc(x,alsoLikesDict), x] for x in xs]

        # appends a list of visitors who have read the document
        for k in xs_sort:
            userUUIDs = []
            for x in alsoLikesDict:
                for docUUID in alsoLikesDict[x]:
                    if docUUID == k[1]:
                        userUUIDs.append(x)
            k[1] = k[1]
            k.append(userUUIDs)

        # sort() method sorts on first element of nested list 
        xs_sort.sort()
        # reverse the list to get most read document first
        xs_sort.reverse()

        return xs_sort

    @dispatch(object, object, object)
    def alsoLikes(self, docUUID, userUUID, sortFunc):
        alsoLikesDict = {}
        userUUIDS = self.readersOfDoc(docUUID)
        for user in userUUIDS:
            if user == userUUID:
                alsoLikesDict.update({userUUID: [docUUID]})
            else:
                alsoLikesDict.update({user: self.docsReadByVisitor(user)})
        
        # xs is the set of all read document UUIDs, and because its a set it gets rid of duplicates
        xs = set([])
        for k in alsoLikesDict.keys():
            # gets the list of document UUIDs associated with a key k and adds them to the set xs
            xs = xs | set(alsoLikesDict[k])
        xs_sort = [[sortFunc(x,alsoLikesDict), x] for x in xs]

        # appends a list of visitors who have read the document
        for k in xs_sort:
            userUUIDs = []
            for x in alsoLikesDict:
                for docUUID in alsoLikesDict[x]:
                    if docUUID == k[1]:
                        userUUIDs.append(x)
            k.append(userUUIDs)
            # get the last 4 hex-digits of the document UUID
            k[1] = k[1]

        # sort on a tuple sorts on the first element
        xs_sort.sort()
        xs_sort.reverse()

        return xs_sort
    

# view = Views2()
# view.set_file_name("sample_100k_lines.json")
# print(view.alsoLikes("100806162735-00000000115598650cb8b514246272b5", "00000000deadbeef", view.sortFunc))

