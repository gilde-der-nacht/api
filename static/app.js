'use strict';

// TODO put all functions into an object and remove ugly app_ prefix
// TODO is async & fetch to new?

async function app_status() {
	// TODO make a function for get, which may also check the status code and throw exceptions
	const response = await fetch('/status');
	const json = await response.json();
	return json;
}

function verifyUid(uid) {
	return true;
}

function verifyBody(body) {
	return true;
}

async function app_ressourceAdd(ressourceUid, publicBody, privateBody) {
	verifyUid(ressourceUid);
	verifyBody(publicBody);
	verifyBody(privateBody);
	throw 'Not Implemented';
}

async function app_ressourcelistAll(ressourceUid) {
	verifyUid(ressourceUid);
	const path = `/ressource/${ressourceUid}`;
	throw 'Not Implemented';
}
