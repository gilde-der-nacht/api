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

    static async get(path, username=undefined, password=undefined) {
        const response = await fetch(path, {
            method: 'GET',
            mode: 'cors',
        });
        const text = await response.text();
        return [text, response.status];
    }
    
    static async getWithAuthorization(path, username, password) {
        const response = await fetch(path, {
            method: 'GET',
            mode: 'cors',
            headers: {
                'Authorization': 'Basic ' + btoa(username + ":" + password),
            }
        });
        const text = await response.text();
        return [text, response.status];
    }    

    static async post(path, data) {
        const response = await fetch(path, {
            method: 'POST',
            mode: 'cors',
            body: data,
        });
        const text = await response.text();
        return [text, response.status];
    }

    static async put(path, data) {
        const response = await fetch(path, {
            method: 'PUT',
            mode: 'cors',
            body: data,
        });
        const text = await response.text();
        return [text, response.status];
    }

    static async delete(path) {
        const response = await fetch(path, {
            method: 'DELETE',
            mode: 'cors',
        });
        const text = await response.text();
        return [text, response.status];
    }
}

/*
Function should be part of JavaScript language and is quite likely used by
users of Olymp.

At the moment only ascending ordering is implemented.

Usage:

result = sortBy(array, item => item.field);

See:

https://lodash.com/docs/#sortBy
https://ramdajs.com/docs/#sortBy

*/
function sortBy(array, ...criterias) {
    const result = array.slice(0);
    result.sort((a, b) => {
        for(let i = 0; i < criterias.length; i += 1) {
            const ca = criterias[i](a);
            const cb = criterias[i](b);
            if((i < criterias.length) && (ca === cb)) {
                continue;
            }
            return ca > cb ? 1 : -1; // > = ascending, < = descending
        }
    });
    return result;
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
            this.server = origin.includes('127.0.0.1') ? 'http://127.0.0.1:5000' :'https://api.gildedernacht.ch';
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
        return RegExp('^[0-9a-f]{64}$').test(uid);
    }

    static _verifyIdentification(value) {
        return (typeof value) === 'string';
    }

    static _verifyBody(body) {
        return (typeof body) === 'object';
    }

    async status() {
        const path = `${this.server}/status`;
        const [text, status] = await HTTP.get(path);
        if(status !== HTTP.CODES.OK_200) {
            throw 'Status - Invalid Response';
        }
        return JSON.parse(text);
    }

    async entriesAdd(resourceUid, identification, publicBody, privateBody) {
        Olymp._verify(Olymp._verifyUid(resourceUid));
        Olymp._verify(Olymp._verifyIdentification(identification));
        Olymp._verify(Olymp._verifyBody(publicBody));
        Olymp._verify(Olymp._verifyBody(privateBody));
        const path = `${this.server}/resources/${resourceUid}/entries`;
        const data = {
            identification: identification,
            publicBody: publicBody,
            privateBody: privateBody,
        };
        const [_, status] = await HTTP.post(path, JSON.stringify(data));
        if(status !== HTTP.CODES.CREATED_201) {
            throw 'Add - Invalid Response';
        }
    }

    async entriesList(resourceUid) {
        Olymp._verify(Olymp._verifyUid(resourceUid));
        const path = `${this.server}/resources/${resourceUid}/entries`;
        //const [text, status] = await HTTP.getWithAuthorization(path, 'name', 'pw');
        const [text, status] = await HTTP.get(path);
        if(status !== HTTP.CODES.OK_200) {
            throw 'List - Invalid Response';
        }
        return JSON.parse(text);
    }
}

/*
(Should) behave exactly like Olymp, but does not need a connection to the backend.
*/
class OlympMock {
    constructor(config) {
        this.entries = {};
        this.authenticated = true; // TODO add configuration option to change this
        this.localStorage = false; // TODO add coonfiguration option to use local storage for persistent testing
        this.load();
        this.resourceAdd(RESOURCE_UID_TEST);
    }

    // TODO unify constructor/clear
    clear() {
        this.entries = {};
        this.resourceAdd(RESOURCE_UID_TEST);
        this.save();
    }

    load() {
        if(this.localStorage) {
            try {
                this.entries = JSON.parse(window.localStorage.getItem('entries'));
            } catch {
                this.entries = {};
            }
        }
    }

    save() {
        if(this.localStorage) {
            window.localStorage.setItem('entries', JSON.stringify(this.entries));
        }
    }

    static async delay(milliseconds) {
        return new Promise((resolve) => setTimeout(resolve, milliseconds));
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
        };
    }

    async resourceAdd(resourceUid) {
        if(!(resourceUid in this.entries)) {
            this.entries[resourceUid] = [];
        }
    }

    async entriesAdd(resourceUid, identification, publicBody, privateBody, timestamp=undefined) {
        const entryUid = OlympMock.createUid();
        const entry = {
            resourceUid: resourceUid,
            entryUid: entryUid,
            identification: identification,
            timestamp: timestamp === undefined ? OlympMock.createTimestamp() : timestamp,
            publicBody: publicBody,
            privateBody: privateBody,
            url: '',
            userAgent: '',
        };
        this.entries[resourceUid].push(entry);
        this.save();
        /*
        Locally generated timestamps are not in microseconds and therefore not unique,
        especially because there is no delay due an network connection.
        So add an artifical delay.
        */
        const delayMilliseconds = 10;
        await OlympMock.delay(delayMilliseconds);
        return entryUid;
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
        }

        const grouped = groupBy(entries, callee); // e.g. entry => entry.publicBody.userId
        const entriesNewest = Object.keys(grouped).map(key => {
            const entries = grouped[key];
            entries.sort((lhs, rhs) => lhs.timestamp < rhs.timestamp ? 1 : -1);
            return entries[0]; // only take the newest
        });
        return entriesNewest;
    }

    async entriesList(resourceUid) {
        const unfiltered = this.entries[resourceUid];
        return OlympMock.filterMostRecent(unfiltered, item => item.identification);
    }
}
