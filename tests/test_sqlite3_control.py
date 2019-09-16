import os
import unittest
import time
from interface.control import DBControlInterface


class MySQLControlTest(unittest.TestCase):

    def setUp(self):

        self.command_stored_in_buffer = "select * from track_lines;"
        self.db = DBControlInterface("sqlite3", db_nickname="city_line")
        self.db.connect()

    def test_table(self):

        self.assertIsInstance(self.db.get_table(), list)

    def test_Help(self):

        self.assertIsInstance(self.db.get_help(), str)

    def test_SQL(self):

        self.assertIsInstance(
            self.db.get_sql("""select * from cities"""), 
            list
        )

    def test_R(self):

        self.db.command_stored_in_buffer = self.command_stored_in_buffer
        self.assertEqual(
            self.db.get_r(),
            "Your Previous Command is: {}".format(self.command_stored_in_buffer)
        )

    def test_T(self):

        self.db.command_stored_in_buffer = self.command_stored_in_buffer
        self.assertIsInstance(
            self.db.get_t(),
            list
        )

    def test_Command(self):

        command_dict = {
            "db": list,
            "help": str,
            "r": str,
            "t": str,
            "table": list,
            "sql": (
                "select * from track_lines",
                list
            )
        }

        for key, value in command_dict.items():

            if key == "sql":

                self.assertIsInstance(
                    self.db.command_interface(
                        value[0],
                    ),
                    value[1]
                )

            else:
                self.assertIsInstance(
                    self.db.command_interface(
                        key
                    ),
                    value
                )
    
    def test_save(self):

        self.db.get_save(["select * from track_lines", "test_track_lines.csv"])
        
        time.sleep(0.5)

        self.assertTrue(
            os.path.exists("csv_file/test_track_lines.csv")
        )

    def test_city(self):
    
        self.assertIsInstance(
            self.db.get_city(),
            list  
        )
    
    def test_any_table(self):
        
        self.assertIsInstance(
            self.db.get_any_table("track_lines"),
            list   
        )
