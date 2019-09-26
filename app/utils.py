import os
from interface.control import DBControlInterface


def get_data_from_db(db_client: DBControlInterface, incoming_data: str) -> (list, list):
    
    if os.environ["DB_TYPE"] == "sqlite3":

        sqlite3_client = DBControlInterface(
            "sqlite3", db_nickname=os.environ["DB_NAME"]
        ) 
        
        sqlite3_client.connect()
        return_data = sqlite3_client.command_interface("""{}""".format(incoming_data))

        return [x[0] for x in sqlite3_client.cursor.description], return_data

    return_data = db_client.command_interface(
        """{}""".format(incoming_data)
    )

    return [x[0] for x in db_client.cursor.description], return_data
