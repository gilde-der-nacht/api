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
    int(uid, 16)


def entries_add(resource_uid, public_body, private_body, url, user_agent):
    verify_uid(resource_uid)

    entry_uid = generate_uid()
    timestamp = generate_timestamp()

    insert_entry_sql = '''
        INSERT INTO entries (resource_uid, entry_uid, timestamp, public_body, private_body, url, user_agent) VALUES (?, ?, ?, ?, ?, ?, ?)
    '''

    conn, cur = connect(DB_PATH)
    cur.execute(insert_entry_sql, [resource_uid, entry_uid, timestamp, public_body, private_body, url, user_agent])
    conn.commit()
    conn.close()

    return {'uid': entry_uid, 'timestamp': timestamp}


def entries_list(resource_uid):
    verify_uid(resource_uid)

    select_resource_sql = '''
        SELECT resource_uid, entry_uid, timestamp, public_body, private_body, url, user_agent FROM entries WHERE resource_uid = ?
    '''

    conn, cur = connect(DB_PATH)
    cur.execute(select_resource_sql, [resource_uid])
    results = cur.fetchall()
    conn.close()

    return results


def connect(path):
    conn = sqlite3.connect(path, isolation_level=None)
    return conn, conn.cursor()


def setup():
    reset_tables_sql = '''
        DROP TABLE IF EXISTS resources;
        DROP TABLE IF EXISTS entries;
    '''

    create_tables_sql = '''
        CREATE TABLE resources (
            resource_uid TEXT UNIQUE NOT NULL,
            timestamp TEXT NOT NULL,
            public_body TEXT NOT NULL,
            private_body TEXT NOT NULL,
            url TEXT NOT NULL,
            user_agent TEXT NOT NULL
        );
        CREATE TABLE entries (
            resource_uid TEXT NOT NULL,
            entry_uid TEXT UNIQUE NOT NULL,
            timestamp TEXT NOT NULL,
            public_body TEXT NOT NULL,
            private_body TEXT NOT NULL,
            url TEXT NOT NULL,
            user_agent TEXT NOT NULL,
            FOREIGN KEY (resource_uid) REFERENCES resources (resource_uid)
        );
    '''

    conn, cur = connect(DB_PATH)
    cur.executescript(reset_tables_sql + create_tables_sql)
    conn.close()


def resources_add(resource_uid, public_body, private_body, url, user_agent):
    timestamp = generate_timestamp()
    insert_resource_sql = '''
        INSERT INTO resources (resource_uid, timestamp, public_body, private_body, url, user_agent) VALUES (?, ?, ?, ?, ?, ?)
    '''

    conn, cur = connect(DB_PATH)
    cur.execute(insert_resource_sql, [resource_uid, timestamp, public_body, private_body, url, user_agent])
    conn.close()


def resources_list():
    select_resource_sql = '''
        SELECT resource_uid, timestamp, public_body, private_body, url, user_agent FROM resources
    '''

    conn, cur = connect(DB_PATH)
    cur.execute(select_resource_sql)
    results = cur.fetchall()
    conn.close()

    return results


if __name__ == '__main__':
    setup()

    # test resource

    assert len(resources_list()) == 0
    UID_TEST = '0000000000000000000000000000000000000000000000000000000000000000'
    resources_add(UID_TEST, '{}', '{}', '', '')
    assert len(resources_list()) == 1

    # test entries

    PUBLIC = '{"a": 1}'
    PRIVATE = '{"b": 2}'
    N = 5
    assert len(entries_list(UID_TEST)) == 0
    for i in range(N):
        entries_add(UID_TEST, PUBLIC, PRIVATE, '', '')
    assert len(entries_list(UID_TEST)) == 5

    print(entries_list(UID_TEST)[0])
    assert entries_list(UID_TEST)[0][3] == PUBLIC
    assert entries_list(UID_TEST)[0][4] == PRIVATE

    # add useful resource

    UID_ROLLENSPIELTAGE = resources_add('095da522f49aebbd35443fd2349d578a1aaf4a9ea05ae7d59383a5f416d4fd3b', '{"description": "Luzerner Rollenspieltage 2019"}', '{"email": "mail@rollenspieltage.ch"}', '', '')
