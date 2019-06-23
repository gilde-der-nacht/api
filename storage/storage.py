#!/usr/bin/env python3
import json
import os
import sqlite3
import secrets
import datetime

LENGTH_OF_UID = 32
STORAGE_PATH = os.path.dirname(os.path.abspath(__file__))
DB_PATH = STORAGE_PATH + '/database.sqlite3'


def generate_uid():
    return secrets.token_hex(LENGTH_OF_UID)


def generate_timestamp():
    return str(datetime.datetime.now().isoformat())


def verify_uid(uid):
    if len(uid) != (2 * LENGTH_OF_UID):
        raise ValueError('Invalid Resource ID')
    return int(uid, 16)


def write(resource_uid, public_body, private_body, url, user_agent):
    verify_uid(resource_uid)

    entry_uid = generate_uid()
    timestamp = generate_timestamp()

    conn, cur = connect(DB_PATH)

    insert_entry_sql = """
        INSERT INTO entries (resource_uid, entry_uid, timestamp, url, user_agent, public_body, private_body) VALUES (?, ?, ?, ?, ?, ?, ?)
    """
    cur.execute(insert_entry_sql, (resource_uid, entry_uid, timestamp, url, user_agent, public_body, private_body))

    conn.commit()
    conn.close()

    return {'uid': entry_uid, 'timestamp': timestamp}


def read(resource_uid):
    verify_uid(resource_uid)

    conn, cur = connect(DB_PATH)

    select_resource_sql = """
        SELECT resource_uid, entry_uid, timestamp, url, user_agent, public_body, private_body FROM entries WHERE resource_uid = ?
    """

    cur.execute(select_resource_sql, [resource_uid])
    results = cur.fetchall()

    conn.close()

    return results


def connect(path):
    conn = sqlite3.connect(path, isolation_level=None)
    return conn, conn.cursor()


def setup():
    conn, cur = connect(DB_PATH)

    reset_tables_sql = """
        DROP TABLE IF EXISTS resources;
        DROP TABLE IF EXISTS entries;
    """

    create_tables_sql = """
        CREATE TABLE resources (
            resource_uid TEXT UNIQUE NOT NULL,
            timestamp TEXT NOT NULL,
            url TEXT NOT NULL,
            user_agent TEXT NOT NULL,
            public_body TEXT NOT NULL,
            private_body TEXT NOT NULL
        );
            CREATE TABLE entries (
            resource_uid TEXT NOT NULL,
            entry_uid TEXT UNIQUE NOT NULL,
            timestamp TEXT NOT NULL,
            url TEXT NOT NULL,
            user_agent TEXT NOT NULL,
            public_body TEXT NOT NULL,
            private_body TEXT NOT NULL,
            FOREIGN KEY (resource_uid) REFERENCES resources (resource_uid)
        );
    """

    cur.executescript(reset_tables_sql + create_tables_sql)
    conn.close()


def generate_test_resource():
    conn, cur = connect(DB_PATH)

    insert_resource_sql = """
        INSERT INTO resources (resource_uid, timestamp, url, user_agent, public_body, private_body) VALUES (?, ?, ?, ?, ?, ?)
    """

    cur.execute(insert_resource_sql, ('095da522f49aebbd35443fd2349d578a1aaf4a9ea05ae7d59383a5f416d4fd3b', '2019-06-22T15:28:47.358620', '', '', '{"description": "Luzerner Rollenspieltage 2019"}', '{"email": "mail@rollenspieltage.ch"}'))
    conn.close()


def read_test_resource(resource_uid):
    conn, cur = connect(DB_PATH)

    select_resource_sql = """
        SELECT resource_uid, timestamp, url, user_agent, public_body, private_body FROM resources WHERE resource_uid = ?
    """

    cur.execute(select_resource_sql, [resource_uid])
    results = cur.fetchall()

    conn.close()

    return results


if __name__ == '__main__':
    setup()
    generate_test_resource()

    # uid1 = generate_uid()
    # print(uid1)
    #
    # timestamp = generate_timestamp()
    # print(timestamp)
    #
    # public_write = '{"a": 1}'
    # private_write = '{"b": 2}'
    #
    # write(uid1, public_write, private_write)
    # uid1_read, entry_uid1, public_read, private_read, timestamp = read(uid1)[0]
    #
    # assert uid1_read == uid1
    # assert public_write == public_read
    # assert private_write == private_read
