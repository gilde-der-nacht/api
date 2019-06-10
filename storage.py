#!/usr/bin/env python3
import json
import sqlite3
import secrets
import datetime

length_of_uid = 64
database_path = 'database.sqlite3'


def generate_uid():
    return secrets.token_hex(length_of_uid)


def generate_timestamp():
    return str(datetime.datetime.now())  # TODO is the format guaranteed? or is better to explicitly specify it?


def verify_parameters(container_uid):
    if len(container_uid) != 2 * length_of_uid:
        raise ValueError('Invalid Container ID')


def verify_json(json_string):
    json.loads(json_string)


def write(container_uid, public_data, private_data):
    verify_parameters(container_uid)
    verify_json(public_data)
    verify_json(private_data)

    entry_uid = generate_uid()
    timestamp = generate_timestamp()

    db = db_connect(database_path)

    insert_entry_sql = """
        INSERT INTO gdn_database (container_uid, entry_uid, public_body, private_body, timestamp) VALUES (?, ?, ? , ?, ?)
    """
    db.execute(insert_entry_sql, (container_uid, entry_uid, public_data, private_data, timestamp))
    print("written")
    print(container_uid)
    print(entry_uid)
    print(public_data)
    print(private_data)
    print(timestamp)


def read(container_uid):
    verify_parameters(container_uid)

    db = db_connect(database_path)

    select_container_sql = """
        SELECT container_uid, entry_uid, public_body, private_body, timestamp FROM gdn_database WHERE container_uid = ?
    """

    db.execute(select_container_sql, [container_uid])
    results = db.fetchall()

    print(results)
    for row in results:
        print(row)

    # TODO: Create one JSON to return

    # timestamp = ''
    # entry_uid = ''
    # public = ''
    # private = ''
    # return entry_uid, timestamp, public, private


def db_connect(db_file):
    conn = sqlite3.connect(db_file)
    # conn.row_factory = sqlite3.Row
    return conn.cursor()


def setup():
    db = db_connect(database_path)

    reset_tables_sql = 'DROP TABLE IF EXISTS gdn_database;'
    db.execute(reset_tables_sql)

    create_tables_sql = """
        CREATE TABLE gdn_database (
            container_uid TEXT NOT NULL,
            entry_uid TEXT NOT NULL,
            public_body TEXT NOT NULL,
            private_body TEXT NOT NULL, 
            timestamp TEXT NOT NULL
        )
    """
    db.execute(create_tables_sql)


if __name__ == '__main__':
    setup()

    uid1 = generate_uid()
    print(uid1)

    timestamp = generate_timestamp()
    print(timestamp)

    public_write = '{"a": 1}'
    private_write = '{"b": 2}'

    write(uid1, public_write, private_write)
    read(uid1)

    # assert (public_write == public_read)
    # assert (private_write == private_read)
