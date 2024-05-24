"""This module have DatabaseManager class (that handles
all database operations) and main func(that sends quries
to DBManager for performing and then saving results)"""

import argparse
import logging
import os
import time
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError


class DatabaseManager:
    """Class that performs all required operations with DB.
    Such as checking connection, creating tables, loading data,
    performing queries and saving results"""

    def __init__(self, user, password, db_name, host, port):
        self.engine = create_engine(
            f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{db_name}"
        )
        self.wait_for_postgres()

    def wait_for_postgres(self):
        """Waiting database connection"""
        while True:
            try:
                conn = self.engine.connect()
                logging.info("Database is available.")
                conn.close()
                return True
            except OperationalError:
                logging.info("Database is unavailable. Retry after 1 second.")
                time.sleep(1)

    def create_tables(self):
        """Creating tables for storing datasets"""
        with self.engine.begin() as conn:
            conn.exec_driver_sql("DROP TABLE IF EXISTS rooms CASCADE")
            conn.exec_driver_sql("DROP TABLE IF EXISTS students")
            with open("create_queries/create_rooms.sql", "r", encoding="utf-8") as file:
                conn.exec_driver_sql(file.read())
                logging.info("Created rooms table")
            with open(
                "create_queries/create_students.sql", "r", encoding="utf-8"
            ) as file:
                conn.exec_driver_sql(file.read())
                logging.info("Created students table")

    def json_to_database(self, json_path: str):
        """Loading json file into DB as rows in table

        Args:
            json_path (str): path to json file that u want to load in DB
        """

        df = pd.read_json(json_path)
        table_name = Path(json_path).stem
        df.to_sql(table_name, index=False, con=self.engine, if_exists="append")
        logging.info(f"Loaded data from {json_path} to {table_name} table")

    def fill_db(self, students_path: str, rooms_path: str):
        """Sending all json files for loading in DB

        Args:
            students_path (str): path to students.json file
            rooms_path (str): path to rooms.json file
        """

        self.json_to_database(rooms_path)
        self.json_to_database(students_path)

    def do_query(self, query_path: str, saving_format: str):
        """Performing given query and saving results in json

        Args:
            query_path (str): path to sql file with query u want to perform
            saving_format (str): format for output results json/xml
        """

        with open(query_path, "r", encoding="utf-8") as file:
            query = file.read()
            df = pd.read_sql(query, con=self.engine)
            logging.info(f"Query performed and saved in dataframe")
            query_name = Path(query_path).stem
            output_dir = Path(f"results/{query_name}")
            output_dir.mkdir(parents=True, exist_ok=True)

            if saving_format == "json":
                df.to_json(
                    output_dir / f"{query_name}_results.json",
                    orient="records",
                    indent=4,
                )
            elif saving_format == "xml":
                df.to_xml(
                    output_dir / f"{query_name}_results.xml",
                    pretty_print=True,
                    index=False,
                )
            logging.info(
                f"Results of query {query_path} saved in {output_dir / f"{query_name}_results."}{saving_format}"
            )


def parse_arguments():
    """Parsing command lane arguments and returning them
    in one object (obj.students, obj.rooms, obj.format)"""

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-s", "--students", help="Path to students file", metavar="path"
    )
    parser.add_argument("-r", "--rooms", help="Path to rooms file", metavar="path")
    parser.add_argument("-f", "--format", help="Output format", choices=["xml", "json"])
    return parser.parse_args()


def get_env():
    """Returning Tuple of enviroment variables
    (USER_NAME, USER_PASS, DB_NAME, HOST, PORT)"""

    load_dotenv()
    return (
        os.getenv("USER_NAME"),
        os.getenv("USER_PASS"),
        os.getenv("DB_NAME"),
        os.getenv("HOST"),
        os.getenv("PORT"),
    )


if __name__ == "__main__":
    output_logs_dir = Path(f"results/logs")
    if not os.path.exists(output_logs_dir):
        os.makedirs(output_logs_dir)
    logging.basicConfig(
        level=logging.INFO,
        filename="results/logs/logs.log",
        format="%(asctime)s %(levelname)s %(message)s",
    )
    USER_NAME, USER_PASS, DB_NAME, HOST, PORT = get_env()
    args = parse_arguments()
    db_manager = DatabaseManager(USER_NAME, USER_PASS, DB_NAME, HOST, PORT)
    db_manager.create_tables()
    db_manager.fill_db(args.students, args.rooms)

    for q in ("query1.sql", "query2.sql", "query3.sql", "query4.sql"):
        db_manager.do_query(f"task_queries/{q}", args.format)
