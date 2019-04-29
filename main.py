import json
import os
import re
import sys
from interface.view import initial_interface
from interface.view import database_interface
from tools.init import init_db


def db_main(sql_lib_definition_dict: dict):

    database_type, database_nickname = None, None

    print("\nWelcome to the Universal SQL Client:\n")

    if len(sys.argv) < 3:

        database_type, database_nickname = initial_interface()

    else:

        database_type = sql_lib_definition_dict[sys.argv[1]]
        database_nickname = sys.argv[2]

    database_interface(database_type, database_nickname)


def main():

    sql_lib_definition_dict = None

    with open("config/db_definition.json", "r") as definition_obj:

        sql_lib_definition_dict = json.loads(
            definition_obj.read()
        )
        
    if len(sys.argv) >= 2 and len(sys.argv) <= 3:

        if re.search(r"^(?i)(init|del)$", sys.argv[1]):

            init_db()
        
        else:

            db_main(sql_lib_definition_dict)

        #Clear the environment variable after the webapp
        del os.environ["DB_NAME"]
        del os.environ["DB_TYPE"]
    
    elif len(sys.argv) > 3 and len(sys.argv) <= 4:

        if sys.argv[1] == "webapp":

            os.environ["DB_TYPE"] = sql_lib_definition_dict[sys.argv[2]]
            os.environ["DB_NAME"] = sys.argv[3]
        
            from app.webapp import app

            app.run(host="127.0.0.1", port=5000)

    else:

        print(
        """
        Help:

            python init.py init                                 -- to create a DB metadata
            python init.py del <db_nickname>                    -- to delete a DB metadata

            e.g. python init.py del yahoo_1223

            python main.py <sql_engine>                         -- to enter the client prompt
            python main.py <sql_engine> <db_nickname>           -- to connect a DB's client prompt

            e.g.
            python main.py mysql yahoo_1223

            Webapp
            python main.py webapp <sql_engine> <db_nickname>    -- to run webapp

        """
        )


if __name__ == "__main__":

    main()