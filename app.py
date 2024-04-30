import pandas as pd
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv
import argparse


def json_to_database(json_path: str, engine):
    df = pd.read_json(json_path)
    table_name = json_path.split('/')[-1].split('.')[0]
    df.to_sql(
    table_name,
    index=False,
    con=engine,
    if_exists='append'
    )


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-s','--students',help='Path to students file', metavar='path')
    parser.add_argument('-r','--rooms',help='Path to rooms file', metavar='path')
    parser.add_argument('-f','--format ',help='Output format', choices=['xml','json'])
    return parser.parse_args()


def get_env():
    load_dotenv()
    return os.getenv('USER_NAME'), os.getenv('USER_PASS'), os.getenv('DB_NAME'), os.getenv('HOST'), os.getenv('PORT')


if __name__ == '__main__':
    USER_NAME, USER_PASS, DB_NAME, HOST, PORT = get_env()

    parse_arguments()

    engine = create_engine(
    f'postgresql+psycopg2://{USER_NAME}:{USER_PASS}@{HOST}:{PORT}/{DB_NAME}'
    )
