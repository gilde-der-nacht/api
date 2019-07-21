'use strict';

/*
This script is full of somewhat more modern JavaScript:

async/await, fetch, class, ...

If there is problem that not all devices support this newer this JavaScript
keywords, this script itself can be "compiled" to an older JavaScript standard with

Babel

https://babeljs.io/

sudo npm install @babel/core @babel/cli @babel/preset-env

babel olymp.js
*/

/*
A thin wrapper around the Fetch API

https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API/Using_Fetch
*/
class HTTP {
    static get CODES() {
        return {
            CONTINUE_100: 100,
            SWITCHING_PROTOCOLS_101: 101,
            OK_200: 200,
            CREATED_201: 201,
            ACCEPTED_202: 202,
            NON_AUTHORITATIVE_INFORMATION_203: 203,
            NO_CONTENT_204: 204,
            RESET_CONTENT_205: 205,
            PARTIAL_CONTENT_206: 206,
            MULTIPLE_CHOICES_300: 300,
            MOVED_PERMANENTLY_301: 301,
            FOUND_302: 302,
            SEE_OTHER_303: 303,
            NOT_MODIFIED_304: 304,
            USE_PROXY_305: 305,
            RESERVED_306: 306,
            TEMPORARY_REDIRECT_307: 307,
            BAD_REQUEST_400: 400,
            UNAUTHORIZED_401: 401,
            PAYMENT_REQUIRED_402: 402,
            FORBIDDEN_403: 403,
            NOT_FOUND_404: 404,
            METHOD_NOT_ALLOWED_405: 405,
            NOT_ACCEPTABLE_406: 406,
            PROXY_AUTHENTICATION_REQUIRED_407: 407,
            REQUEST_TIMEOUT_408: 408,
            CONFLICT_409: 409,
            GONE_410: 410,
            LENGTH_REQUIRED_411: 411,
            PRECONDITION_FAILED_412: 412,
            REQUEST_ENTITY_TOO_LARGE_413: 413,
            REQUEST_URI_TOO_LONG_414: 414,
            UNSUPPORTED_MEDIA_TYPE_415: 415,
            REQUESTED_RANGE_NOT_SATISFIABLE_416: 416,
            EXPECTATION_FAILED_417: 417,
            PRECONDITION_REQUIRED_428: 428,
            TOO_MANY_REQUESTS_429: 429,
            REQUEST_HEADER_FIELDS_TOO_LARGE_431: 431,
            INTERNAL_SERVER_ERROR_500: 500,
            NOT_IMPLEMENTED_501: 501,
            BAD_GATEWAY_502: 502,
            SERVICE_UNAVAILABLE_503: 503,
            GATEWAY_TIMEOUT_504: 504,
            HTTP_VERSION_NOT_SUPPORTED_505: 505,
            NETWORK_AUTHENTICATION_REQUIRED_511: 511,
        };
    }

    static async get(path) {
        const response = await fetch(path);
        const text = await response.text();
        return [text, response.status]
    }

    static async post(path, data) {
        const response = await fetch(path, {
            method: 'POST',
            body: data,
        });
        const text = await response.text();
        return [text, response.status]
    }

    static async put(path, data) {
        const response = await fetch(path, {
            method: 'PUT',
            body: data,
        });
        const text = await response.text();
        return [text, response.status]
    }

    static async delete(path) {
        const response = await fetch(path, {
            method: 'DELETE',
        });
        const text = await response.text();
        return [text, response.status]
    }
}

// this resource is empty forever
const RESOURCE_UID_EMPTY = 'ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff';

// this resource is just to add anything you like, entries may be deleted occasionally by an administrator
const RESOURCE_UID_TEST = '0000000000000000000000000000000000000000000000000000000000000000';

/*
This is the main class which allows an easy access to the Olymp server.
*/
class Olymp {
    constructor(config) {
        if('server' in config) {
            this.server = config.server;
        } else {
            const origin = document.location.origin;
            this.server = origin.includes('127.0.0.1') ? origin :'https://api.gildedernacht.ch';
        }
    }

    /*
    The _verify functions are not here to protect against malicious intent (which is impossible),
    but to give the user of this class an early feedback if a parameter is invalid.

    At the moment _verifyUid & _verifyBody do not directly call _verify, because both functions
    are tested externally. Something which may reveal too much details.
    */

    static _verify(condition) {
        if(!condition) {
            throw 'Invalid Parameter';
        }
    }

    static _verifyUid(uid) {
        return (uid.length === 64) && RegExp('[0-9a-f]{64}').test(uid)
    }

    static _verifyBody(body) {
        return (typeof body) === 'object';
    }

    async status() {
        const path = `${this.server}/status`;
        const [text, status] = await HTTP.get(path);
        if(status !== HTTP.CODES.OK_200) {
            throw 'Invalid Response';
        }
        return JSON.parse(text);
    }

    async entriesAdd(resourceUid, identificationUid, publicBody, privateBody) {
        Olymp._verify(Olymp._verifyUid(resourceUid));
        Olymp._verify(Olymp._verifyUid(identificationUid));
        Olymp._verify(Olymp._verifyBody(publicBody));
        Olymp._verify(Olymp._verifyBody(privateBody));
        const path = `${this.server}/resources/${resourceUid}/entries`;
        const data = {
            identificationUid: identificationUid,
            publicBody: publicBody,
            privateBody: privateBody,
        };
        const [_, status] = await HTTP.post(path, JSON.stringify(data));
        if(status !== HTTP.CODES.CREATED_201) {
            throw 'Invalid Response';
        }
    }

    async entriesList(resourceUid) {
        Olymp._verify(Olymp._verifyUid(resourceUid));
        const path = `${this.server}/resources/${resourceUid}/entries`;
        const [text, status] = await HTTP.get(path);
        if(status !== HTTP.CODES.OK_200) {
            throw 'Invalid Response';
        }
        return JSON.parse(text);
    }

    static filterMostRecent(entries, callee) {
        // as GROUP BY from SQL or a groupBy from functional libraries like https://lodash.com/docs/#groupBy or https://ramdajs.com/docs/#groupBy
        function groupBy(array, iteratee) {
            return array.reduce((acc, item) => {
                const key = iteratee(item);
                if(!(key in acc)) {
                    acc[key] = [];
                }
                acc[key].push(item);
                return acc;
            }, {});
        };

        const grouped = groupBy(entries, callee); // e.g. entry => entry.publicBody.userId
        const entriesNewest = Object.keys(grouped).map(key => {
            const entries = grouped[key];
            entries.sort((lhs, rhs) => lhs.timestamp < rhs.timestamp);
            return entries[0]; // only take the newest
        });
        return entriesNewest;
    }

    static hexlify(buffer) {
        return [...new Uint8Array(buffer)].map(byte => {
            return byte.toString(16).padStart(2, '0');
        }).join('');
    }

    /*
    If a user registers itself several times, there should be a possibility to detect this.
    Because the Olymp server has, by design (maybe this need to be changed), no understanding
    of the content of the data it stores, this needs to done on the client.
    To do this, the client needs some unique information from the user. Possibilites are:

    firstname + surname, email:

    This would mean that the client has e.g. the email of all people registered, which would be awfull,
    as all email addresses are revealed to the public.

    Hash of firstname/surname/email:

    Information is not directly revealed. But everyone who has an idea who is atending the event may
    do the hashing by themself. Especeially because there is no salting, someone could do that in advance.

    Salt+Hash of firstname/surname/email:

    What is the salt? Ideally there should be a different salt per user, but because the server
    has no idea about a user, this is not so easy possible. Salt = resource UID? Not ideal.
    As the salt is always public information this just makes the process harder.

    Portability?

    https://developer.mozilla.org/en-US/docs/Web/API/SubtleCrypto/digest
    https://www.npmjs.com/package/js-sha256
    */
    static async hash(value, salt) {
        // TODO at least proper PBKDF2
        const encoder = new TextEncoder();
        const data = encoder.encode(value + salt);
        const result = await window.crypto.subtle.digest('SHA-256', data);
        return Olymp.hexlify(result);
    }
}

/*
(Should) behave exactly like Olymp, but does not need a connection to the backend.
*/
class OlympMock {
    constructor(config) {
        this.entries = {};
        this.authenticated = true; // TODO add configuration option to change this
        this.resourceAdd(RESOURCE_UID_TEST);
    }

    static async delay(milliseconds) {
        return new Promise((resolve) => setTimeout(resolve, milliseconds))
    }

    static createTimestamp() {
        return new Date(Date.now()).toISOString().slice(0, -1);
    }

    static createUid() {
        return 'TEST-UID'; // TODO randomize
    }

    async status() {
        return {
            time: OlympMock.createTimestamp(),
            version: '0.0.0',
        }
    }

    async resourceAdd(resourceUid) {
        this.entries[resourceUid] = [];
    }

    async entriesAdd(resourceUid, identificationUid, publicBody, privateBody, timestamp=undefined) {
        const entryUid = OlympMock.createUid();
        const entry = {
            resourceUid: resourceUid,
            entryUid: entryUid,
            identificationUid: identificationUid,
            timestamp: timestamp === undefined ? OlympMock.createTimestamp() : timestamp,
            publicBody: publicBody,
            privateBody: privateBody,
            url: '',
            userAgent: '',
        }
        this.entries[resourceUid].push(entry);
        /*
        Locally generated timestamps are not in microseconds and therefore not unique,
        especially because there is no delay due an network connection.
        */
        await OlympMock.delay(10);
        return entryUid;
    }

    async entriesList(resourceUid) {
        return this.entries[resourceUid];
    }
};
