import os
import re
import sys
import time
from .control import DBInterface


exit_command_list = ["q", "quit", "x", "exit"]


def front_prompt(database_type: str=None, database_nickname: str=None):


    def platform_prompt(platform_name: str) -> str:

        platform_prompt_str = None

        if re.search(r"^(linux*|freebsd*|openbsd*|darwin*)$", platform_name):

            platform_prompt_str = "{0}:{1}".format(
                os.environ["USER"],
                os.environ["HOME"]
            )

        elif platform_name == "win32":

            platform_prompt_str = "{0}:{1}".format(
                os.environ["USERNAME"],
                os.environ["USERDOMAIN"]
            )            

        return platform_prompt_str


    default_prompt_str = "{0} ".format(
        str(time.ctime(time.time())),
    )

    
    if database_type:

        if database_nickname:

            default_prompt_str += "{0} {1} {2}> ".format(
                database_type,
                database_nickname,
                platform_prompt(sys.platform)
            )

        else:

            default_prompt_str += "{0} {1}> ".format(
                database_type,
                platform_prompt(sys.platform)
            )

    else:

        default_prompt_str += "{0}> ".format(
            platform_prompt(sys.platform)
        )

    return input(default_prompt_str)


def database_interface(database_type: str, db_nickname: str=None):

    command_buffer = None

    command_keys = [
        "r", #return to previous command
        "t", #execute previous command
        "table", #display table inside the database
        "db", #List out all the registered database
        "help", #Look for help
        "h" #Look for help 
    ]

    if db_nickname:
    
        received_command = front_prompt(database_type, db_nickname)
    
    else:

        received_command = front_prompt(database_type)

    os.environ["DB_TYPE"] = database_type

    if database_type == "sqlite3":

        db_client = DBInterface("sqlite3", sqlite3_filename=db_nickname)
        os.environ["DB_NAME"] = db_nickname

    else:        
    
        db_client = DBInterface(database_type, db_nickname=db_nickname)
        os.environ["DB_NAME"] = db_nickname

    db_client.connect()

    while (received_command not in exit_command_list):

        try:

            if re.search(r"switch \w+$", received_command):

                database_interface(database_type, received_command.split(" ")[1])

            else:

                db_client.command_interface(received_command, command_buffer)

        except Exception as error:

            print(error)

        if not (received_command in command_keys):

            command_buffer = received_command
        
        received_command = front_prompt(database_type, db_nickname)


def initial_interface() -> str:

    command = front_prompt()

    while command not in exit_command_list:

        if re.search(r"^connect\s([\w\s])+\s?([\w\s])*$", command):

            return command.split(" ")[1:]

        else:

            print("You are not connected to any registered DB")

        command = front_prompt()

    exit(1)

