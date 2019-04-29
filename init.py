import getpass
import json
import re
import sys


def init_install():

    db_meta = dict()
    db_type = input("Please enter your db_type: ")
    
    db_nickname = input("Please give a nickname for your definition: ")
    
    if db_nickname or len(db_nickname) > 0:

        db_meta[db_nickname] = dict()

    else:

        print("Empty Nickname")
        exit(1)

    temp = {}

    temp["db_name"] = input("Please enter your db_name: ")

    if db_type != "sqlite3":
    
        temp["server"] = input("Please enter your db_hostname: ")
        temp["username"] = input("Please enter your db_username: ")
        temp["password"] = getpass.getpass("Please enter your db_password: ")
    

    count = 0
    empty_key = []

    for key, value in temp.items():

        if not value or len(value) == 0:

            empty_key.append(key)
            print("{} is empty".format(key))

            count += 1
    
    if count > 0:

        print(
            "These attributes have empty entries: {}".format(
                ','.join(empty_key)
            )
        )
        exit(1)

    else:

        config_data = None
        db_meta[db_nickname].update(temp)

        with open("config/config.json", "r") as config_file:

            config_data = json.loads(config_file.read())
    
        config_data.update(db_meta)
    
    with open("config/config.json", "w", newline="") as config_file:

        config_file.write(
            json.dumps(config_data, indent=4)
        )
    
def delete_db_meta(db_nickname):

    config_data = None
        

    with open("config/config.json", "r") as config_file:

        config_data = json.loads(config_file.read())
    
    del config_data[db_nickname]

    with open("config/config.json", "w", newline="") as config_file:

        config_file.write(
            json.dumps(config_data, indent=4)
        )


def init_db():

    if len(sys.argv) < 2 or len(sys.argv) > 3:

        print("python init.py init")
        print("python init.py del <db_nickname>")

    else:

        if re.search(r"^(?i)init$", sys.argv[-1]) and len(sys.argv) == 2:

            init_install()
        
        elif re.search(r"^(?i)del$", sys.argv[1]) and len(sys.argv) == 3:

            delete_db_meta(sys.argv[-1])
    
        else:

            print("Invalid parameters")


init_db()
