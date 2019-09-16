import unittest
from database.models import DataBaseEngine


class TestModelSqlite3(unittest.TestCase):

    def setUp(self):

        self.db_engine = DataBaseEngine("sqlite3", "city_line")
        self.db_engine.connect()
    
    def test_table(self):
        
        self.assertIsInstance(
            self.db_engine.retrieve_table(),
            list
        )

    def test_sql(self):

        self.db_engine.execute("select * from track_lines")
        self.assertIsInstance(
            self.db_engine.cursor.fetchall(),
            list
        )
