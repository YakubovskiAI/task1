import unittest
from pathlib import Path
from unittest.mock import MagicMock, call, patch

from sqlalchemy.exc import OperationalError, TimeoutError

from app import DatabaseManager


class TestDatabaseManager(unittest.TestCase):

    @patch.object(DatabaseManager, "wait_for_postgres")
    @patch("app.create_engine")
    def setUp(self, mock_create_engine: MagicMock, mock_wait_for_postgres: MagicMock):
        self.dbman = DatabaseManager("user", "password", "db_name", "host", "port")

    def test_wait_for_postgres_success(self):
        self.assertTrue(self.dbman.wait_for_postgres())

    def test_wait_for_postgres_fail(self):
        self.dbman.engine.connect.side_effect = OperationalError(None, None, None)
        self.assertRaises(TimeoutError, self.dbman.wait_for_postgres)

    @patch("app.open")
    def test_create_tables(self, mock_open: MagicMock):
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

    @patch("app.pd.read_json")
    def test_json_to_database(self, mock_read_json: MagicMock):
        path = "data/rooms.json"
        self.dbman.json_to_database(path)
        mock_to_sql = mock_read_json.return_value.to_sql
        mock_read_json.assert_any_call(path)
        mock_to_sql.assert_any_call(
            "rooms", index=False, con=self.dbman.engine, if_exists="append"
        )

    @patch.object(DatabaseManager, "json_to_database")
    def test_fill_db(self, mock_json_to_database: MagicMock):
        path_rooms = "data/rooms.json"
        path_students = "data/students.json"
        self.dbman.fill_db(path_rooms, path_students)
        mock_json_to_database.assert_has_calls(
            [call(path_rooms), call(path_students)], any_order=True
        )

    @patch("app.Path.mkdir")
    @patch("app.pd.read_sql")
    @patch("app.open")
    def test_do_query_json(
        self, mock_open: MagicMock, mock_read_sql: MagicMock, mock_mkdir: MagicMock
    ):
        self.dbman.do_query("data/query1.sql", "json")
        mock_read: MagicMock = mock_open.return_value.__enter__.return_value.read
        mock_to_json: MagicMock = mock_read_sql.return_value.to_json
        mock_open.assert_any_call("data/query1.sql", "r", encoding="utf-8")
        mock_read.assert_called_once_with()
        mock_read_sql.assert_any_call(mock_read.return_value, con=self.dbman.engine)
        mock_mkdir.assert_called_once()
        mock_to_json.assert_called_once()

    @patch("app.Path.mkdir")
    @patch("app.pd.read_sql")
    @patch("app.open")
    def test_do_query_xml(
        self, mock_open: MagicMock, mock_read_sql: MagicMock, mock_mkdir: MagicMock
    ):
        self.dbman.do_query("data/query1.sql", "xml")
        mock_read: MagicMock = mock_open.return_value.__enter__.return_value.read
        mock_to_xml: MagicMock = mock_read_sql.return_value.to_xml
        mock_open.assert_any_call("data/query1.sql", "r", encoding="utf-8")
        mock_read.assert_called_once_with()
        mock_read_sql.assert_any_call(mock_read.return_value, con=self.dbman.engine)
        mock_mkdir.assert_called_once()
        mock_to_xml.assert_called_once()


if __name__ == "__main__":
    unittest.main()
