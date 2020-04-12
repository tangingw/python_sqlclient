import os
import json
import os.path
import re
from importlib import import_module
from typing import List


class DataBaseEngine(object):

    configuration = None

    if os.path.exists("config/config.json"):

        with open("config/config.json", "r") as config_file:

            configuration = json.loads(config_file.read())

    else:

        raise FileNotFoundError

    def __init__(self, db_engine: str, db_nickname=None):

        self.conn = None
        self.cursor = None
        self.db_engine = db_engine
        self.db_nickname = db_nickname    
        #self.sqlite3_filename = sqlite3_filename

    def connect(self):

        if self.db_nickname not in self.configuration:

            print(f"Table {self.db_nickname} Not Found in config.json")

        db_module = import_module(self.db_engine)

        try:        

            if self.db_engine == "sqlite3":

                self.conn = db_module.connect(
                    self.configuration[self.db_nickname]["db_name"]
                )

            else:

                self.conn = db_module.connect(
                    host=self.configuration[self.db_nickname]["server"],
                    database=self.configuration[self.db_nickname]["db_name"],
                    user=self.configuration[self.db_nickname]["username"],
                    password= self.configuration[self.db_nickname]["password"], 
                )

        except db_module.InterfaceError:

            print("DB for {0} Not Found".format(self.db_engine))
            exit(1)
        
        except db_module.OperationalError as e:

            print(e)
            exit(1)

        self.cursor = self.conn.cursor()

    def close(self):

        self.conn.close()

    def execute(self, sql_statement:str):

        self.cursor.execute(sql_statement)

        sql_regex = re.compile(r"^(?i)(CREATE|ALTER|UPDATE|INSERT|DELETE|VIEW|ROLLBACK)$")

        if sql_regex.match(sql_statement.split()[0]):

            self.conn.commit()
    
    def rollback(self):

        self.conn.rollback()
        
    def retrieve_table(self):

        if self.db_engine == "sqlite3":

            retrieve_table_str = """
                select sql from sqlite_master;
            """

        else:

            retrieve_table_str = """
                SELECT DISTINCT TABLE_NAME FROM information_schema.TABLES;
            """

        self.execute(retrieve_table_str)
        return self.cursor.fetchall()
    
    def retrieve_column_name(self, table_name:str) -> List:

        if self.db_engine == "sqlite3":
        
            retrieve_column_str = """
                select * from pragma_table_info({0});
            """.format(table_name)

        else:

            retrieve_column_str = """
                SELECT COLUMN_NAME, ORDINAL_POSITION, DATA_TYPE, NUMERIC_PRECISION, DATETIME_PRECISION, COLLATION_NAME 
                FROM information_schema.COLUMNS WHERE TABLE_NAME = '{0}'
            """.format(table_name)
        
        self.execute(retrieve_column_str)
        return self.cursor.fetchall()
