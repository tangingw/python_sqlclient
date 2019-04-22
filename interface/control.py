import csv
import os
import re
from database.models import DataBaseEngine
from typing import List


class _DBInternalInterface(DataBaseEngine):

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

                        for query in data_from_table[index*line_to_display: (index + 1)*line_to_display]:

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

    def _get_output(self, output=None, delay_mode: bool=False, line_to_display: int=10):

        if output:

            data_from_db = output

        else:

            data_from_db = self.cursor.fetchall()

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

    def _write_to_file(self, filename: str, query_result: List):

        with open("csv_file/{}".format(filename), "w", newline="") as csv_save_file:

            csv_writer = csv.writer(csv_save_file, delimiter=",")

            if self.cursor.description:

                csv_writer.writerow([desc[0] for desc in self.cursor.description])
            
            csv_writer.writerows(query_result)

        print("Query result written to file: {0}".format(filename))

    def _save_query_to_file(self, filename: str, command_stored_in_buffer: str=None, sql_command: str=None):
        
        query_result = None

        if command_stored_in_buffer and re.search(r"(?i)(select)\s.+", command_stored_in_buffer):

            if command_stored_in_buffer.find("|") > -1:

                command_stored_in_buffer = command_stored_in_buffer.split("|")[0]

            if re.search(r"column\s.+", command_stored_in_buffer):

                query_result = self.retrieve_column_name(command_stored_in_buffer.split(" ")[1])
            
            elif re.search(r"table\s.+", command_stored_in_buffer):

                query_result = self.retrieve_table()

            else:

                self.exec(command_stored_in_buffer)
                query_result = self.cursor.fetchall()

        elif sql_command and re.search(r"(?i)(select)\s.+", sql_command):

            self.exec(sql_command)
            query_result = self.cursor.fetchall()
            
        self._write_to_file(filename, query_result)

    def _delay_result_output(self, input_command: str):

        if input_command.find("|") != -1:

            self.exec(input_command.split("|")[0])
            self._get_output(delay_mode=True, line_to_display=10)
        
        else:

            self.exec(input_command)            
            self._get_output()

    def _delay_column_output(self, input_command: str):

        if input_command.find("|") != -1:

            table_name = (input_command.split("|")[0]).split(" ")[1]
            self._get_output(self.retrieve_column_name(table_name), delay_mode=True)

        else:

            table_name = input_command.split(" ")[1]
            self._get_output(self.retrieve_column_name(table_name))


class DBInterface(_DBInternalInterface):

    command_stored_in_buffer = None

    def get_db(self):

        print(list(self.configuration.keys()))
    
    def get_help(self):

        print(
                """
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
            )

    def get_h(self):

        self.get_help()

    def get_table(self):

        self._get_output(self.retrieve_table())

    def get_r(self):

        if (not self.command_stored_in_buffer) or self.command_stored_in_buffer == "r":

                print("No Previous Command Found!")
            
        else:

            print(
                "Your Previous Command is: {}".format(self.command_stored_in_buffer)
            )
    
    def get_t(self):

        if not self.command_stored_in_buffer:

            print("You cannot execute any command")
        
        else:

            buffer_list = self.command_stored_in_buffer.split(" ")

            if hasattr(self, "do_{}".format(buffer_list[0])):

                getattr(self, "do_{}".format(buffer_list)[0])(buffer_list[1:])

            elif self.command_stored_in_buffer.find("|") != -1:

                self._delay_result_output(self.command_stored_in_buffer)

            else:

                self.exec(self.command_stored_in_buffer)
                self._get_output()

    def get_save(self, args_list: list):

        if len(args_list) > 1:

            self._save_query_to_file(
                args_list[-1], #filename 
                sql_command= " ".join(args_list[0:-1]) #sqlcommand
            )

        elif len(args_list) == 1:
        
            if os.path.exists(args_list[0]):

                print("You Have saved your previous query to file: {0}".format(args_list[0]))
            
            else:
                self._save_query_to_file(
                    args_list[0], #filename
                    self.command_stored_in_buffer
                )

    def get_column(self, args_list: list):

        self._delay_column_output(
            "column {}".format(" ".join(args_list))
        )

    def get_webapp(self):

        from app.webapp import app

        app.run(host="127.0.0.1", port=5000)

    def get_sql(self, input_command):

        sql_regex = re.compile(r"^(?i)(ALTER|CREATE|DELETE|INSERT|SELECT|UPDATE)$")

        if sql_regex.match(input_command.split()[0]):

            self._delay_result_output(input_command)
        
        else:

            print("Not a valid SQL Expression!")

    def command_interface(self, input_command: str, command_stored_in_buffer: str):

        input_command_list = input_command.split(" ")
        self.command_stored_in_buffer = command_stored_in_buffer

        if hasattr(self, "get_{}".format(input_command_list[0])):

            instance_method = getattr(self, 
                "get_{}".format(input_command_list[0])
            )

            if len(input_command_list) == 1:

                instance_method()

            elif len(input_command_list) > 1:

                instance_method(input_command_list[1:])

        else:

            self.get_sql(input_command)