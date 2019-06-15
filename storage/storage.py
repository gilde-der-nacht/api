#!/usr/bin/env python3

import sqlite3
import secrets
import datetime

# the status code constants are all uppercase, this are lowercase, just decide for one
length_of_uid = 32
database_path = 'storage/database.sqlite3'


def generate_uid():
    return secrets.token_hex(length_of_uid)


def generate_timestamp():
    return str(datetime.datetime.now())  # TODO is the format guaranteed? or is better to explicitly specify it? now().isoformat?


def verify_uid(container_uid):
    if len(container_uid) != (2 * length_of_uid):
        raise ValueError('Invalid Container ID')
    # TODO test if it a hexstring -> just do int(string, 16) -> gives also ValueError


def write(public_data, private_data, container_uid=None):
    verify_uid(container_uid)

    entry_uid = generate_uid()
    timestamp = generate_timestamp()

    conn, cur = db_connect(database_path)

    # TODO still a mix of body/data

    insert_entry_sql = """
        INSERT INTO entries (container_uid, entry_uid, public_body, private_body, timestamp) VALUES (?, ?, ?, ?, ?)
    """
    cur.execute(insert_entry_sql, (container_uid, entry_uid, public_data, private_data, timestamp))

    conn.commit()
    conn.close()


def read(container_uid):
    verify_uid(container_uid)

    conn, cur = db_connect(database_path)

    select_container_sql = """
        SELECT container_uid, entry_uid, public_body, private_body, timestamp FROM entries WHERE container_uid = ?
    """

    cur.execute(select_container_sql, [container_uid])
    results = cur.fetchall()

    conn.close()

    return results


def db_connect(db_file):
    # TODO sometimes called file, sometimes called path, what is it?
    # TODO why has this method a prefix, the other ones not?
    # TODO even if it is called db_connect, why is the parameter has a prefix?

    conn = sqlite3.connect(db_file)
    return conn, conn.cursor()


def setup():
    conn, cur = db_connect(database_path)

    reset_resources_tables_sql = """
        DROP TABLE IF EXISTS resources;
        """
    cur.execute(reset_resources_tables_sql)

    reset_entries_tables_sql = """
        DROP TABLE IF EXISTS entries;
        """
    cur.execute(reset_entries_tables_sql)

    create_resources_tables_sql = """
        CREATE TABLE resources (
            resource_uid TEXT UNIQUE NOT NULL,
            timestamp TEXT NOT NULL,
            url TEXT NOT NULL,
            user_agent TEXT NOT NULL,
            public_body TEXT NOT NULL,
            private_body TEXT NOT NULL
        )
        """
    cur.execute(create_resources_tables_sql)

    create_entries_tables_sql = """
        CREATE TABLE entries (
            resource_uid TEXT NOT NULL,
            entry_uid TEXT UNIQUE NOT NULL,
            timestamp TEXT NOT NULL,
            url TEXT NOT NULL,
            user_agent TEXT NOT NULL,
            public_body TEXT NOT NULL,
            private_body TEXT NOT NULL,
            FOREIGN KEY (resource_uid) REFERENCES resources (resource_uid)
        )
        """
    cur.execute(create_entries_tables_sql)

    # TODO all this command can be merged into one command and sent to the database at once

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
