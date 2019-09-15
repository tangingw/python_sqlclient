import csv
import json
import os
import re
import waitress
from database.models import DataBaseEngine
from typing import List


def parse_lambda(key, value, func):

    if value["parameters"]:

        return lambda x: func(
            """{}""".format(value["sql"]).format(x)
        )

    return lambda : func("""{}""".format(value["sql"]))


class DBControlInterface(DataBaseEngine):

    command_stored_in_buffer = None
    defined_attributes = None

    if os.path.exists("config/command_def.json"):
    
        with open("config/command_def.json", "r") as def_file:

            defined_attributes = json.loads(def_file.read())

    def __init__(self, db_engine: str, db_nickname=None):

        if db_nickname:

            for key, value in self.defined_attributes[db_nickname].items():
                
                setattr(
                    self,
                    "get_{}".format(key),
                    parse_lambda(key, value, self.get_sql)
                )
                
        super().__init__(db_engine, db_nickname=db_nickname)

    def _write_to_file(self, filename: str, query_result: List):

        with open("csv_file/{}".format(filename), "w", newline="") as csv_save_file:

            csv_writer = csv.writer(csv_save_file, delimiter=",")

            if self.cursor.description:

                csv_writer.writerow([desc[0] for desc in self.cursor.description])
            
            csv_writer.writerows(query_result)

        return "Query result written to file: {0}".format(filename)

    def _save_query_to_file(self, filename: str, sql_command: str=None):
        
        query_result = None
        command_buffer = None

        if self.command_stored_in_buffer:

            if self.command_stored_in_buffer.find("|") > -1:

                command_buffer = self.command_stored_in_buffer.split("|")[0]

            else:

                command_buffer = self.command_stored_in_buffer

            query_result = self.command_interface(command_buffer)

        elif sql_command and re.search(r"(?i)(select)\s.+", sql_command):

            query_result = self.command_interface(sql_command)
            
        self._write_to_file(filename, query_result)

    def get_db(self):

        return list(self.configuration.keys())
    
    def get_help(self):

        return """
            Help:
                e                                   -- exeucte the previous command
                p                                   -- show previous command
                db                                  -- list out all the registered db
                exit/x                              -- same as quit
                help/h                              -- list out the command
                quit/q                              -- quit
                table                               -- list out the table within the db
                column <TABLE_NAME>                 -- show the attribute of the table
                connect <DB_NAME>                   -- connect to the designated db
                switch <DB_NAME>                    -- switch from current db to designated db
                save <FILENAME.csv>                 -- save previous query result to CSV file
                save <SQL QUERY> <FILENAME.csv>     -- save query result to CSV file
                webapp                              -- spawn a webapp at http://127.0.0.1:5000/sql_webapp

                Funky mode:
                    |  -- This is similar to unix/linux "more" or "less" command:
                    e.g. select * from table_123; |
                    This will display the first 10 entries from the select/table/column query
                    To display remaining queries, press "<" or ">"
                    To quit from Funky mode, press x
            """

    def get_h(self):

        return self.get_help()

    def get_table(self):

        return self.retrieve_table()

    def get_r(self):

        if (not self.command_stored_in_buffer) or self.command_stored_in_buffer == "r":

            return "No Previous Command Found!"

        return "Your Previous Command is: {}".format(self.command_stored_in_buffer)
            
    def get_t(self):

        if not self.command_stored_in_buffer:

            return "You cannot execute any command"
        
        else:

            buffer_list = self.command_stored_in_buffer.split(" ")

            if hasattr(self, "do_{}".format(buffer_list[0])):

                return getattr(self, "do_{}".format(buffer_list)[0])(buffer_list[1:])

            self.execute(self.command_stored_in_buffer)
            return self.cursor.fetchall()

    def get_save(self, args_list: list):

        if os.path.exists(args_list[0]):
    
            return "You Have saved your previous query to file: {0}".format(args_list[0])
        
        else:

            if len(args_list) > 1:

                self._save_query_to_file(
                    args_list[-1], #filename 
                    sql_command= " ".join(args_list[0:-1]) #sqlcommand
                )

            elif len(args_list) == 1:
        
                self._save_query_to_file(
                    args_list[0], #filename
                    self.command_stored_in_buffer
                )

            return "File {} written successfully".format(args_list[0])

    def get_column(self, table_name: str):

        return self.retrieve_column_name(table_name[0])

    def get_rollback(self):

        self.rollback()
        return "Rollback is trigger!"

    def get_webapp(self):

        from app.webapp import app

        app.run(host="127.0.0.1", port=5000)

    def get_sql(self, input_command):

        sql_regex = re.compile(r"^(ALTER|CREATE|DELETE|INSERT|SELECT|UPDATE)$")

        if sql_regex.match(input_command.split()[0].upper()):

            self.execute(input_command)
            return self.cursor.fetchall()

        return "Not a valid SQL Expression!"

    def get_falcon(self):

        from app.webapp_falcon import app

        waitress.serve(app, host='127.0.0.1', port=8041, url_scheme='https')

    #def command_interface(self, input_command: str, command_stored_in_buffer: str):
    def command_interface(self, input_command: str):

        input_command_list = input_command.split(" ")

        if hasattr(self, "get_{}".format(input_command_list[0])):

            instance_method = getattr(self, 
                "get_{}".format(input_command_list[0])
            )

            if len(input_command_list) == 1:
                
                return instance_method()

            elif len(input_command_list) > 1: 
                
                if input_command_list[0] in ["save", "column"]:

                    return instance_method(input_command_list[1:])

                #elif input_command_list[0] == "table":

                #    return instance_method()

                elif input_command_list[0] in [
                    key for key in self.defined_attributes.keys() 
                    if dict(self.defined_attributes)[key]["parameters"]]:
                    
                    return instance_method(input_command_list[1])

        return self.get_sql(input_command)


class DBInterface(DBControlInterface):

    def _delay_mode(self, data_from_table: List, line_to_display=20):

        data_length = len(data_from_table)

        if data_length < line_to_display:

            for data in data_from_table:

                print("|".join([str(item) for item in data]))
            
        else:

            index = 0
            next_input = ">"

            while True:

                if next_input == ">":

                    if index < int(len(data_from_table)/line_to_display) + 1:

                        init_index, final_index = index*line_to_display, (index + 1)*line_to_display

                        for query in data_from_table[init_index: final_index]:

                            print("|".join([str(item) for item in query]))

                        index += 1

                    else:

                        print("You are at the bottom of the page")

                elif next_input == "<":

                    if index != 0:

                        index -= 1

                        for query in data_from_table[index*line_to_display: (index + 1)*line_to_display]:

                            print("|".join([str(item) for item in query]))

                    else:

                        print("You are at the top of the page")
                
                elif next_input == "x":

                    break

                else:

                    print("{0} is not recognized!".format(next_input))

                next_input = input("""\nPress '<' or '>' to continue: """)

    def _get_output(self, data_from_db=None, delay_mode: bool=False, line_to_display: int=10):

        #print("\n")
        if isinstance(data_from_db, str):

            if len(data_from_db) > 0:

                print("{}\n".format(data_from_db))
        
        elif isinstance(data_from_db, tuple) or isinstance(data_from_db, list):

            print("\n")
            table_header = "|".join([desc[0] for desc in self.cursor.description])

            print(table_header)
            print("_" * len(table_header))

            if delay_mode:

                self._delay_mode(data_from_db, line_to_display)
            
            else:

                for query in data_from_db:

                    print("|".join([str(entry) for entry in query]))
            
            print("\n")

    
    def get_result_output(self, input_command: str, command_stored_in_buffer):

        self.command_stored_in_buffer = command_stored_in_buffer

        if len(input_command) == 0:

            pass

        elif input_command.find("|") != -1:

            self._get_output(
                data_from_db=self.command_interface(
                    input_command.split("|")[0], 
                ),
                delay_mode=True, 
                line_to_display=10
            )
        
        else:
           
            self._get_output(
                data_from_db=self.command_interface(
                    input_command
                )
            )

    