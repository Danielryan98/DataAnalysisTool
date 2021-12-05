#Library imports
import tkinter as tk
import sys, getopt, re

#Class imports
from gui import GUI
from data_gui import DataGUI

def main(argv):
    user_uuid = ""
    doc_uuid = ""
    task_id = ""
    file_name = ""
    try:
        # string of option letter that the program recognises. Options that require an argument are followed by a semicolon
        opts, args = getopt.getopt(sys.argv[1:], "hu:d:t:f:")
    except getopt.GetoptError:
        print("Usage:")
        print("")
        print("cw2 -u <user_uuid> -d <doc_uuid> -t <task_id> -f <file_name>")
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print("cw2 -u <user_uuid> -d <doc_uuid> -t <task_id> -f <file_name>")
            sys.exit()
        elif opt == '-u':
            user_uuid = arg
        elif opt == '-d':
            doc_uuid = arg
        elif opt == '-t':
            task_id = arg
        elif opt == '-f':
            file_name = arg

    # run task
    if task_id == "2a":
        check_doc_id(doc_uuid)
        root = tk.Tk()
        data_gui = DataGUI(root, file_name)
        data_gui.by_country_plot(doc_uuid)
        root.mainloop()
    elif task_id == "2b":
        check_doc_id(doc_uuid)
        root = tk.Tk()
        data_gui = DataGUI(root, file_name)
        data_gui.by_continent_plot(doc_uuid)
        root.mainloop()
    elif task_id == "3a":
        root = tk.Tk()
        data_gui = DataGUI(root, file_name)
        data_gui.by_browser_plot()
        root.mainloop()
    elif task_id == "3b":
        root = tk.Tk()
        data_gui = DataGUI(root, file_name)
        data_gui.by_browser_plot()
        root.mainloop()
    elif task_id == "4":
        root = tk.Tk()
        data_gui = DataGUI(root, file_name)
        data_gui.reader_profiles()
        root.mainloop()
    elif task_id == "5d":
        check_doc_id(doc_uuid)
        check_user_id(user_uuid)
        root = tk.Tk()
        data_gui = DataGUI(root, file_name)
        data_gui.also_likes(doc_uuid, user_uuid)
        root.mainloop()
    elif task_id == "6":
        check_doc_id(doc_uuid)
        check_user_id(user_uuid)
        root = tk.Tk()
        data_gui = DataGUI(root, file_name)
        data_gui.also_likes_graph(doc_uuid, user_uuid)
        root.mainloop()
    elif task_id == "7":
        root = tk.Tk()
        data_gui = GUI(root)
        root.mainloop()


def check_doc_id(doc_id):
    valid = re.findall("^([0-9]{12})-([a-z]|[0-9]){32}$", doc_id)
    if not valid:
        print("Not a valid document UUID. Please run the program again and enter a valid document UUID")
        print("Usage:")
        print("cw2 -u <user_uuid> -d <doc_uuid> -t <task_id> -f <file_name>")
        sys.exit()

def check_user_id(user_id):
    valid = re.findall("^([0-9]|[a-z]){16}$", user_id)
    if not valid:
        print("Not a valid user UUID. Please run the program again and enter a valid user UUID")
        print("Usage:")
        print("cw2 -u <user_uuid> -d <doc_uuid> -t <task_id> -f <file_name>")
        sys.exit()

if __name__ == "__main__":
   main(sys.argv[1:])