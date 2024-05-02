import pandas as pd
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv
import argparse
from pathlib import Path


def json_to_database(json_path: str, engine):
    df = pd.read_json(json_path)
    table_name = json_path.split('/')[-1].split('.')[0]
    df.to_sql(
    table_name,
    index=False,
    con=engine,
    if_exists='append'
    )


def fill_db(students_path: str, rooms_path: str, engine):
    with engine.begin() as conn:
        conn.exec_driver_sql("TRUNCATE TABLE rooms CASCADE")
    json_to_database(rooms_path, engine)
    json_to_database(students_path, engine)




def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-s','--students',help='Path to students file', metavar='path')
    parser.add_argument('-r','--rooms',help='Path to rooms file', metavar='path')
    parser.add_argument('-f','--format',help='Output format', choices=['xml','json'])
    return parser.parse_args()


def get_env():
    load_dotenv()
    return os.getenv('USER_NAME'), os.getenv('USER_PASS'), os.getenv('DB_NAME'), os.getenv('HOST'), os.getenv('PORT')


def do_query(query_file: str, engine, format: str):
    with open(query_file, 'r') as file:
        query = file.read()
        df = pd.read_sql(query,con=engine)
        query_name = query_file.split('.')[0]
        output_dir = Path(f'results/{query_name}')
        output_dir.mkdir(parents=True, exist_ok=True)
        
        if format == 'json':
            df.to_json(output_dir / f'{query_name}_results.json', orient='records', indent=4)
        elif format == 'xml':
            df.to_xml(output_dir / f'{query_name}_results.xml', pretty_print=True, index=False)


if __name__ == '__main__':
    USER_NAME, USER_PASS, DB_NAME, HOST, PORT = get_env()
    args = parse_arguments()
    engine = create_engine(f'postgresql+psycopg2://{USER_NAME}:{USER_PASS}@{HOST}:{PORT}/{DB_NAME}')
    fill_db(args.students, args.rooms, engine)

    for q in ('query1.sql', 'query2.sql', 'query3.sql', 'query4.sql'):
        do_query(q, engine, args.format)
