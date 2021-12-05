#Library imports
import json
import pycountry_convert as pc
import httpagentparser as hp
from multipledispatch import dispatch

class Views:
    def __init__(self):
        self.data_list = []
        self.file_name = ""
        self.browser_dict = {}
        self.browser_names_dict = {}
        self.countries_dict = {}
        self.continents_dict = {}
        self.users_dict = {} 
        self.delete_list = []
        self.history_dict = {}
        self.current_doc_uuid = ""
        self.current_vis_uuid = ""
        self.BROWSER_FULL = "FULL"
        self.BROWSER_SHORT = "SHORT"

    def set_file_name(self, file_name):
        self.file_name = file_name
        for line in open(self.file_name, 'r'):
            self.data_list.append(json.loads(line))

    def clear_data(self):
        self.browser_dict.clear()
        self.browser_names_dict.clear()
        self.countries_dict.clear()
        self.continents_dict.clear()
        self.users_dict.clear()
        self.delete_list.clear()

    # uses the subject_doc_id to uniquely specify a document
    def by_country(self, doc_uuid):
        self.clear_data()
        for entry in self.data_list:
            for k, v in entry.items():
                if v == doc_uuid:
                    if entry["visitor_country"] not in self.countries_dict:
                        self.countries_dict.update({entry["visitor_country"]: 1})
                    else:
                        self.countries_dict[entry["visitor_country"]] = self.countries_dict[entry["visitor_country"]] + 1    
            # not all entries have the "subject_doc_id key so need to check for it otherwise KeyError exception is thrown"
            if "subject_doc_id" in entry and entry["subject_doc_id"] == doc_uuid:
                if entry["visitor_country"] not in self.countries_dict:
                    self.countries_dict.update({entry["visitor_country"]: 1})
                else:
                    self.countries_dict[entry["visitor_country"]] = self.countries_dict[entry["visitor_country"]] + 1
        return self.countries_dict

    def by_continent(self, doc_uuid):
        self.clear_data()
        for entry in self.data_list:
            if "subject_doc_id" in entry and entry["subject_doc_id"] == doc_uuid:
                continent = pc.country_alpha2_to_continent_code(entry["visitor_country"])
                if continent not in self.continents_dict:
                    self.continents_dict.update({continent: 1})
                else:
                    self.continents_dict[continent] = self.continents_dict[continent] + 1
        return self.continents_dict

    #Needs refactored
    def by_browser(self, type):
        self.clear_data()
        for entry in self.data_list:
            if entry["visitor_useragent"] not in self.browser_dict:
                self.browser_dict.update({entry["visitor_useragent"]: 1})
            else:
                self.browser_dict[entry["visitor_useragent"]] = self.browser_dict[entry["visitor_useragent"]] + 1
        print(self.browser_dict.values())
        if type == self.BROWSER_SHORT:
            for entry in self.browser_dict:
                entry_data = hp.detect(entry)
                if 'browser' in entry_data:
                    x = entry_data.get("browser")
                    x = x.get('name')
                    if x not in self.browser_names_dict:
                        self.browser_names_dict.update({x: 1})
                    else:
                        self.browser_names_dict[x] = self.browser_names_dict[x] + 1
            self.browser_names_dict["Other"] = 0
            for browser, count in self.browser_names_dict.items():
                if count < 50:
                    self.browser_names_dict["Other"] += count
                    self.delete_list.append(browser)
            for browser in self.delete_list:
                del self.browser_names_dict[browser]
            return self.browser_names_dict
        else:
            return self.browser_dict

    def user_minutes(self):
        self.clear_data()
        for entry in self.data_list:
            # not all entries have even_readtime key so first check for it here
            if "event_readtime" in entry:
                # then can add the user to the users dict if they don't already exist with time as a key
                if entry["visitor_uuid"] not in self.users_dict:
                    self.users_dict.update({entry["visitor_uuid"]: entry["event_readtime"]})
                else:
                    # if the user exists already then update the time value
                    self.users_dict[entry["visitor_uuid"]] += entry["event_readtime"]
        # then sort the dict by time value in descending order
        self.users_dict = (dict(sorted(self.users_dict.items(), key=lambda item: item[1], reverse=True)))
        return self.users_dict

    def readers_of_doc(self, doc_uuid):
        user_uuids = []
        for entry in self.data_list:
            if entry["event_type"] == "read" and entry["subject_doc_id"] == doc_uuid:
                user_uuids.append(entry["visitor_uuid"])
        return user_uuids

    def docs_read_by_visitor(self, vis_uuid):
        # a user can read the same document multiple times (as is the case for the doc_uuid and user_uuid used for the 2nd 100k lines test)
        # so make a set to get rid of duplicates
        doc_uuids = []
        for entry in self.data_list:
            if entry["event_type"] == "read" and entry["visitor_uuid"] == vis_uuid:
                if entry["subject_doc_id"] not in doc_uuids:
                    doc_uuids.append(entry["subject_doc_id"])
        return doc_uuids

    def sort_func(self, x, dict):
        n = 0
        for k in dict.keys():
            if x in dict[k]:
                n += 1
        return n

    @dispatch(object, object)
    def also_likes(self, doc_uuid, sort_func):
        also_likes_dict = {}
        user_uuids = self.readers_of_doc(doc_uuid)
        for user in user_uuids:
            also_likes_dict.update({user: self.docs_read_by_visitor(user)})
        
        # xs is the set of all read document UUIDs, and because its a set it gets rid of duplicates
        xs = set([])
        for k in also_likes_dict.keys():
            # gets the list of document UUIDs associated with a key k and adds them to the set xs
            xs = xs | set(also_likes_dict[k])
        xs_sort = [[sort_func(x,also_likes_dict), x] for x in xs]

        # appends a list of visitors who have read the document
        for k in xs_sort:
            user_uuids = []
            for x in also_likes_dict:
                for doc_uuid in also_likes_dict[x]:
                    if doc_uuid == k[1]:
                        user_uuids.append(x)
            k.append(user_uuids)

        # sort() method sorts on first element of nested list 
        xs_sort.sort()
        # reverse the list to get most read document first
        xs_sort.reverse()

        return xs_sort

    @dispatch(object, object, object)
    def also_likes(self, doc_uuid, user_uuid, sort_func):
        also_likes_dict = {}
        user_uuids = self.readers_of_doc(doc_uuid)
        for user in user_uuids:
            if user == user_uuid:
                also_likes_dict.update({user_uuid: [doc_uuid]})
            else:
                also_likes_dict.update({user: self.docs_read_by_visitor(user)})
        
        # xs is the set of all read document UUIDs, and because its a set it gets rid of duplicates
        xs = set([])
        for k in also_likes_dict.keys():
            # gets the list of document UUIDs associated with a key k and adds them to the set xs
            xs = xs | set(also_likes_dict[k])
        xs_sort = [[sort_func(x,also_likes_dict), x] for x in xs]

        # appends a list of visitors who have read the document
        for k in xs_sort:
            user_uuids = []
            for x in also_likes_dict:
                for doc_uuid in also_likes_dict[x]:
                    if doc_uuid == k[1]:
                        user_uuids.append(x)
            k.append(user_uuids)

        # sort on a tuple sorts on the first element
        xs_sort.sort()
        xs_sort.reverse()

        return xs_sort
    



