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


def entries_add(resource_uid, identification, public_body, private_body, url, user_agent):
    verify_uid(resource_uid)

    entry_uid = generate_uid()
    timestamp = generate_timestamp()

    insert_entry_sql = '''
        INSERT INTO entries (resource_uid, entry_uid, timestamp, identification, public_body, private_body, url, user_agent) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    '''

    conn, cur = connect(DB_PATH)
    cur.execute(insert_entry_sql,
                [resource_uid, entry_uid, timestamp, identification, public_body, private_body, url, user_agent])
    conn.commit()
    conn.close()

    return {'uid': entry_uid, 'timestamp': timestamp}


def entries_list(resource_uid):
    verify_uid(resource_uid)

    select_resource_sql = '''
        SELECT resource_uid, entry_uid, timestamp, identification, public_body, private_body, url, user_agent FROM entries WHERE resource_uid = ? ORDER BY timestamp
    '''

    conn, cur = connect(DB_PATH)
    cur.execute(select_resource_sql, [resource_uid])
    results = cur.fetchall()
    conn.close()

    return results


def connect(path):
    conn = sqlite3.connect(path, isolation_level=None)
    cur = conn.cursor()
    cur.execute('PRAGMA foreign_keys = ON')  # due to backward compatibility sqlite disabled foreign keys by default
    return conn, cur


# TODO maybe remove this in the future, or add a special parameter to not accidentaly run this?
def drop():
    drop_tables_sql = '''
        DROP TABLE IF EXISTS entries;
        DROP TABLE IF EXISTS resources;
    '''

    conn, cur = connect(DB_PATH)
    cur.executescript(drop_tables_sql)
    conn.close()


def create():
    create_tables_sql = '''
        CREATE TABLE IF NOT EXISTS resources (
            resource_uid TEXT UNIQUE NOT NULL,
            timestamp TEXT NOT NULL,
            public_body TEXT NOT NULL,
            private_body TEXT NOT NULL,
            url TEXT NOT NULL,
            user_agent TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS entries (
            resource_uid TEXT NOT NULL,
            entry_uid TEXT UNIQUE NOT NULL,
            timestamp TEXT NOT NULL,
            identification TEXT NOT NULL,
            public_body TEXT NOT NULL,
            private_body TEXT NOT NULL,
            url TEXT NOT NULL,
            user_agent TEXT NOT NULL,
            FOREIGN KEY (resource_uid) REFERENCES resources (resource_uid)
        );
    '''

    conn, cur = connect(DB_PATH)
    cur.executescript(create_tables_sql)
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


def resources_list_single(resource_uid):
    all_resources = resources_list()
    for resource in all_resources:
        if resource_uid == resource[0]:
            return resource


if __name__ == '__main__':
    # TODO maybe make a backup first, once we run the hot version?

    drop()
    create()

    UID_EMPTY = 'ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff'
    UID_TEST = '0000000000000000000000000000000000000000000000000000000000000000'

    # add one ressource

    assert len(resources_list()) == 0
    resources_add(UID_TEST, '{}', '{}', '', '')
    assert len(resources_list()) == 1

    # test UID_TEST

    PUBLIC = '{"a": 1}'
    PRIVATE = '{"b": 2}'
    N = 3
    assert len(entries_list(UID_TEST)) == 0
    for i in range(N):
        entries_add(UID_TEST, generate_uid(), PUBLIC, PRIVATE, '', '')
    assert len(entries_list(UID_TEST)) == N

    assert entries_list(UID_TEST)[0][4] == PUBLIC
    assert entries_list(UID_TEST)[0][5] == PRIVATE

    # test UID_EMPTY

    assert len(entries_list(UID_EMPTY)) == 0
