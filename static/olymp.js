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

    /*
    Ideally this HTTP codes would be a "static const" part of the HTTP class,
    but this seems to be impossible with the current (2019) JavaScript standards. If anyone
    who reads this has a more JS-alike idea how to express the same idea, please let us know.

    Usage:

    HTTP.CODES().CODE_200_OK
    */
    static CODES() {
        return {
            CODE_100_CONTINUE: 100,
            CODE_101_SWITCHING_PROTOCOLS: 101,
            CODE_200_OK: 200,
            CODE_201_CREATED: 201,
            CODE_202_ACCEPTED: 202,
            CODE_203_NON_AUTHORITATIVE_INFORMATION: 203,
            CODE_204_NO_CONTENT: 204,
            CODE_205_RESET_CONTENT: 205,
            CODE_206_PARTIAL_CONTENT: 206,
            CODE_300_MULTIPLE_CHOICES: 300,
            CODE_301_MOVED_PERMANENTLY: 301,
            CODE_302_FOUND: 302,
            CODE_303_SEE_OTHER: 303,
            CODE_304_NOT_MODIFIED: 304,
            CODE_305_USE_PROXY: 305,
            CODE_306_RESERVED: 306,
            CODE_307_TEMPORARY_REDIRECT: 307,
            CODE_400_BAD_REQUEST: 400,
            CODE_401_UNAUTHORIZED: 401,
            CODE_402_PAYMENT_REQUIRED: 402,
            CODE_403_FORBIDDEN: 403,
            CODE_404_NOT_FOUND: 404,
            CODE_405_METHOD_NOT_ALLOWED: 405,
            CODE_406_NOT_ACCEPTABLE: 406,
            CODE_407_PROXY_AUTHENTICATION_REQUIRED: 407,
            CODE_408_REQUEST_TIMEOUT: 408,
            CODE_409_CONFLICT: 409,
            CODE_410_GONE: 410,
            CODE_411_LENGTH_REQUIRED: 411,
            CODE_412_PRECONDITION_FAILED: 412,
            CODE_413_REQUEST_ENTITY_TOO_LARGE: 413,
            CODE_414_REQUEST_URI_TOO_LONG: 414,
            CODE_415_UNSUPPORTED_MEDIA_TYPE: 415,
            CODE_416_REQUESTED_RANGE_NOT_SATISFIABLE: 416,
            CODE_417_EXPECTATION_FAILED: 417,
            CODE_428_PRECONDITION_REQUIRED: 428,
            CODE_429_TOO_MANY_REQUESTS: 429,
            CODE_431_REQUEST_HEADER_FIELDS_TOO_LARGE: 431,
            CODE_500_INTERNAL_SERVER_ERROR: 500,
            CODE_501_NOT_IMPLEMENTED: 501,
            CODE_502_BAD_GATEWAY: 502,
            CODE_503_SERVICE_UNAVAILABLE: 503,
            CODE_504_GATEWAY_TIMEOUT: 504,
            CODE_505_HTTP_VERSION_NOT_SUPPORTED: 505,
            CODE_511_NETWORK_AUTHENTICATION_REQUIRED: 511,
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

const SERVER = document.location.origin.includes('127.0.0.1') ? document.location.origin :'https://api.gildedernacht.ch';

class Olymp {
    // verify functions are not here to protect against malicious intent (which is impossible), but to give the user of this class an early feedback if a parameter is invalid

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

    static async status() {
        const path = `${SERVER}/status`;
        const [text, status] = await HTTP.get(path);
        if(status !== HTTP.CODES().CODE_200_OK) {
            throw 'Invalid Response';
        }
        return JSON.parse(text);
    }

    static async entriesAdd(resourceUid, publicBody, privateBody) {
        Olymp._verify(Olymp._verifyUid(resourceUid));
        Olymp._verify(Olymp._verifyBody(publicBody));
        Olymp._verify(Olymp._verifyBody(privateBody));
        const path = `${SERVER}/resources/${resourceUid}/entries`;
        const data = {
            'publicBody': publicBody,
            'privateBody': privateBody,
        };
        const [_, status] = await HTTP.post(path, JSON.stringify(data));
        if(status !== HTTP.CODES().CODE_201_CREATED) {
            throw 'Invalid Response';
        }
    }

    static async entriesList(resourceUid) {
        Olymp._verify(Olymp._verifyUid(resourceUid));
        const path = `${SERVER}/resources/${resourceUid}/entries`;
        const [text, status] = await HTTP.get(path);
        if(status !== HTTP.CODES().CODE_200_OK) {
            throw 'Invalid Response';
        }
        return JSON.parse(text);
    }
}
