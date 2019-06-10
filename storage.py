#!/usr/bin/env python3

#import json
import sqlite3
import secrets
import datetime

length_of_uid = 32
database_path = 'database.sqlite3'


def generate_uid():
    return secrets.token_hex(length_of_uid)


def generate_timestamp():
    return str(datetime.datetime.now())  # TODO is the format guaranteed? or is better to explicitly specify it?


def verify_uid(container_uid):
    if len(container_uid) != (2 * length_of_uid):
        raise ValueError('Invalid Container ID')


def verify_json(json_string):
    json.loads(json_string)


def write(container_uid, public_data, private_data):
    verify_uid(container_uid)
    #verify_json(public_data)
    #verify_json(private_data)

    entry_uid = generate_uid()
    timestamp = generate_timestamp()

    conn, cur = db_connect(database_path)

    insert_entry_sql = """
        INSERT INTO gdn_database (container_uid, entry_uid, public_body, private_body, timestamp) VALUES (?, ?, ?, ?, ?)
    """
    cur.execute(insert_entry_sql, (container_uid, entry_uid, public_data, private_data, timestamp))

    conn.commit()
    conn.close()


def read(container_uid):
    verify_uid(container_uid)

    conn, cur = db_connect(database_path)

    select_container_sql = """
        SELECT container_uid, entry_uid, public_body, private_body, timestamp FROM gdn_database WHERE container_uid = ?
    """

    cur.execute(select_container_sql, [container_uid])
    results = cur.fetchall()

    return results

    conn.close()


def db_connect(db_file):
    conn = sqlite3.connect(db_file)
    return conn, conn.cursor()


def setup():
    conn, cur = db_connect(database_path)

    reset_tables_sql = """DROP TABLE IF EXISTS gdn_database"""
    cur.execute(reset_tables_sql)

    create_tables_sql = """
        CREATE TABLE gdn_database (
            container_uid TEXT NOT NULL,
            entry_uid TEXT NOT NULL,
            public_body TEXT NOT NULL,
            private_body TEXT NOT NULL,
            timestamp TEXT NOT NULL
        )
    """
    cur.execute(create_tables_sql)
    conn.close()


if __name__ == '__main__':
    setup()

    uid1 = generate_uid()
    print(uid1)

    timestamp = generate_timestamp()
    print(timestamp)

    public_write = '{"a": 1}'
    private_write = '{"b": 2}'

    write(uid1, public_write, private_write)
    uid1_read, entry_uid1, public_read, private_read, timestamp = read(uid1)[0]

    assert uid1_read == uid1
    assert public_write == public_read
    assert private_write == private_read
