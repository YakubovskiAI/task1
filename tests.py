import unittest
from unittest.mock import patch

from app import DatabaseManager


class TestDatabaseManager(unittest.TestCase):

    @patch.object(DatabaseManager, "wait_for_postgres")
    @patch("app.create_engine")
    def setUp(self, mock_create_engine, mock_wait_for_postgres):
        self.dbman = DatabaseManager("user", "password", "db_name", "host", "port")

    def test_wait_for_postgres(self):
        self.assertTrue(self.dbman.wait_for_postgres())

    @patch("app.open")
    def test_create_tables(self, mock_open):
        mock_conn = self.dbman.engine.begin.return_value.__enter__.return_value
        self.dbman.create_tables()
        mock_conn.exec_driver_sql.assert_any_call("DROP TABLE IF EXISTS rooms CASCADE")
        mock_conn.exec_driver_sql.assert_any_call("DROP TABLE IF EXISTS students")
        mock_open.assert_any_call(
            "create_queries/create_rooms.sql", "r", encoding="utf-8"
        )
        mock_open.assert_any_call(
            "create_queries/create_students.sql", "r", encoding="utf-8"
        )

    # def test_json_to_database(self):
    #     self.dbman.json_to_database('path')


if __name__ == "__main__":
    unittest.main()
