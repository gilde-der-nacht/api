#!/usr/bin/env python3

import sqlite3
import secrets
import datetime

def generate_uid():
	return secrets.token_hex(32)

def generate_timestamp():
	return str(datetime.datetime.now()) # TODO is the format guaranted? or is better to explicitly specify it?

def verify_parameters(container_uid):
	if len(container_uid) != 64:
		raise ValueError('Invalid Container ID')
	# TODO add checks for other parameters

def write(container_uid, public_data, private_data):
	verify_parameters(container_uid)
	entry_uid = generate_uid()
	timestamp = generate_timestamp()

def read(container_uid):
	verify_parameters(container_uid)
	timestamp = ''
	entry_uid = ''
	public = ''
	private = ''
	return entry_uid, timestamp, public, private

def setup():
	pass

if __name__ == '__main__':
	setup()

	uid1 = generate_uid()
	print(uid1)

	timestamp = generate_timestamp()
	print(timestamp)

	public_write = '{"a": 1}'
	private_write = '{"b": 2}'

	write(uid1, public_write, private_write)
	entry_uid, timestamp, public_read, private_read = read(uid1)

	assert(public_write == public_read)
	assert(private_write == private_read)
