import getpass
import json


def init_install():

    db_meta = dict()
    #db_type = input("Please enter your db_type: ")
    
    db_nickname = input("Please give a nickname for your definition: ")
    
    if db_nickname or len(db_nickname) > 0:

        db_meta[db_nickname] = dict()

    else:

        print("Empty Nickname")
        exit(1)

    temp = {}

    temp["server"] = input("Please enter your db_hostname: ")
    temp["username"] = input("Please enter your db_username: ")
    temp["password"] = getpass.getpass("Please enter your db_password: ")
    temp["db_name"] = input("Please enter your db_name: ")

    count = 0

    for key, value in temp.items():

        if not value or len(value) == 0:

            print("{} is empty".format(key))
            count += 1
    
    if count > 0:

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
    

init_install()