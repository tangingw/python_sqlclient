import unittest
from database.models import DataBaseEngine


class TestModelSqlite3(unittest.TestCase):

    def setUp(self):

        self.db_engine = DataBaseEngine("sqlite3", "sqlite3_person")
        self.db_engine.connect()
    
    def test_table(self):
        
        self.assertIsInstance(
            self.db_engine.retrieve_table(),
            list
        )

    def test_sql(self):

        self.db_engine.execute("select * from Person")
        self.assertIsInstance(
            self.db_engine.cursor.fetchall(),
            list
        )


class TestModelMySQL(unittest.TestCase):
    
    def setUp(self):

        self.db_engine = DataBaseEngine("MySQLdb", "radius")
        self.db_engine.connect()
    
    def test_sql(self):

        self.db_engine.execute("select * from radacct")
        self.assertIsInstance(
            self.db_engine.cursor.fetchall(),
            tuple
        )

    def test_column(self):

        self.assertIsInstance(
            self.db_engine.retrieve_column_name("radacct"),
            tuple
        )
    
    def test_table(self):

        self.assertIsInstance(
            self.db_engine.retrieve_table(),
            tuple
        )
