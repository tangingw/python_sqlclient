import os
import unittest
import time
from interface.control_new import DBControlInterface


class ControlTest(unittest.TestCase):

    def setUp(self):

        self.command_stored_in_buffer = "select * from radacct;"
        self.db = DBControlInterface("MySQLdb", db_nickname="radius")
        self.db.connect()

    def test_Column(self):

        self.assertIsInstance(self.db.get_column("radacct"), tuple)

    def test_DB(self):

        self.assertIsInstance(self.db.get_db(), list)

    def test_Help(self):

        self.assertIsInstance(self.db.get_help(), str)

    def test_SQL(self):

        self.assertIsInstance(
            self.db.get_sql(
                """select * from radacct"""
            ), 
            tuple
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
            tuple
        )

    """def test_Command(self):

        command_dict = {
            "db": list,
            "help": str,
            "r": str,
            "t": str,
            "table": tuple,
            "column radacct": tuple,
            "sql": (
                "select * from radacct",
                tuple
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
    """
    
    def test_save(self):

        self.db.get_save(["select * from radacct", "test_radacct.csv"])
        
        time.sleep(0.5)

        self.assertTrue(
            os.path.exists("csv_file/test_radacct.csv")
        )

    def test_nas(self):
    
        self.assertIsInstance(
            self.db.get_nas(),
            tuple   
        )
    
    def test_demo(self):
        
        self.assertIsInstance(
            self.db.get_demo("radacct"),
            tuple   
        )

unittest.main()