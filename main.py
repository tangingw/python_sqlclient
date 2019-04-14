import json
import sys
from interface.view import initial_interface
from interface.view import database_interface


def main():

    database_type, database_nickname = None, None

    sql_lib_definition_dict = None

    with open("config/db_definition.json", "r") as definition_obj:

        sql_lib_definition_dict = json.loads(
            definition_obj.read()
        )
    
    print("\nWelcome to the Universal SQL Client:\n")

    if len(sys.argv) < 3:

        database_type, database_nickname = initial_interface()

    else:

        database_type = sql_lib_definition_dict[sys.argv[1]]
        database_nickname = sys.argv[2]

    database_interface(database_type, database_nickname)


if __name__ == "__main__":

    main()