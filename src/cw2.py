import sys, getopt
from Views import Views
from GUI import GUI

def main(argv):
    user_uuid = ""
    doc_uuid = ""
    task_id = ""
    file_name = ""
    try:
        # string of option letter that the program recognises. Options that require an argument are followed by a semicolon
        opts, args = getopt.getopt(argv, "hu:d:t:f:")
    except getopt.GetoptError:
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

    view = Views(file_name)

    # run task
    if task_id == "2a":
        print(view.bycountry(doc_uuid))
    elif task_id == "2b":
        print(view.bycontinent(doc_uuid))
    elif task_id == "3a":
        print(view.byallbrowser())
    elif task_id == "3b":
        print(view.bybrowser()) # <----------------------------------- returns an empty dict atm. needs fixing
    elif task_id == "4":
        print(view.readerProfile())
    elif task_id == "5d":
        if not user_uuid:
            print(view.alsoLikes(doc_uuid, view.sortFunc))
        else:
            print(view.alsoLikes(doc_uuid, user_uuid, view.sortFunc))
    elif task_id == "6":
        gui = GUI()
    # elif task_id == "7":

if __name__ == "__main__":
   main(sys.argv[1:])