def main(argv):

    user_uuid = ""
    doc_uuid = ""
    task_id = ""

    try:
        opts, args = getopt.getopt(argv, "hu:d:t:f")
    except:
        print()
        