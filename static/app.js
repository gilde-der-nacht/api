'use strict';

/*
async, fetch, class, ... may be too new, babel can be used to convert the scripts

sudo npm install @babel/core @babel/cli @babel/preset-env

babel app.js
*/

// TODO class does not support "static const", any idea?
const HTTP_100_CONTINUE = 100;
const HTTP_101_SWITCHING_PROTOCOLS = 101;
const HTTP_200_OK = 200;
const HTTP_201_CREATED = 201;
const HTTP_202_ACCEPTED = 202;
const HTTP_203_NON_AUTHORITATIVE_INFORMATION = 203;
const HTTP_204_NO_CONTENT = 204;
const HTTP_205_RESET_CONTENT = 205;
const HTTP_206_PARTIAL_CONTENT = 206;
const HTTP_300_MULTIPLE_CHOICES = 300;
const HTTP_301_MOVED_PERMANENTLY = 301;
const HTTP_302_FOUND = 302;
const HTTP_303_SEE_OTHER = 303;
const HTTP_304_NOT_MODIFIED = 304;
const HTTP_305_USE_PROXY = 305;
const HTTP_306_RESERVED = 306;
const HTTP_307_TEMPORARY_REDIRECT = 307;
const HTTP_400_BAD_REQUEST = 400;
const HTTP_401_UNAUTHORIZED = 401;
const HTTP_402_PAYMENT_REQUIRED = 402;
const HTTP_403_FORBIDDEN = 403;
const HTTP_404_NOT_FOUND = 404;
const HTTP_405_METHOD_NOT_ALLOWED = 405;
const HTTP_406_NOT_ACCEPTABLE = 406;
const HTTP_407_PROXY_AUTHENTICATION_REQUIRED = 407;
const HTTP_408_REQUEST_TIMEOUT = 408;
const HTTP_409_CONFLICT = 409;
const HTTP_410_GONE = 410;
const HTTP_411_LENGTH_REQUIRED = 411;
const HTTP_412_PRECONDITION_FAILED = 412;
const HTTP_413_REQUEST_ENTITY_TOO_LARGE = 413;
const HTTP_414_REQUEST_URI_TOO_LONG = 414;
const HTTP_415_UNSUPPORTED_MEDIA_TYPE = 415;
const HTTP_416_REQUESTED_RANGE_NOT_SATISFIABLE = 416;
const HTTP_417_EXPECTATION_FAILED = 417;
const HTTP_428_PRECONDITION_REQUIRED = 428;
const HTTP_429_TOO_MANY_REQUESTS = 429;
const HTTP_431_REQUEST_HEADER_FIELDS_TOO_LARGE = 431;
const HTTP_500_INTERNAL_SERVER_ERROR = 500;
const HTTP_501_NOT_IMPLEMENTED = 501;
const HTTP_502_BAD_GATEWAY = 502;
const HTTP_503_SERVICE_UNAVAILABLE = 503;
const HTTP_504_GATEWAY_TIMEOUT = 504;
const HTTP_505_HTTP_VERSION_NOT_SUPPORTED = 505;
const HTTP_511_NETWORK_AUTHENTICATION_REQUIRED = 511;

class HTTP {
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

// TODO app.js/App are awfull names
class App {
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
        const response = await fetch('/status');
        if(response.status !== HTTP_200_OK) {
            throw 'Invalid Response';
        }
        const json = await response.json();
        return json;
    }

    static async resourceAdd(resourceUid, publicBody, privateBody) {
        App._verify(App._verifyUid(resourceUid));
        App._verify(App._verifyBody(publicBody));
        App._verify(App._verifyBody(privateBody));
        const path = `/resources/${resourceUid}/entries`;
        const data = {
            'publicBody': publicBody,
            'privateBody': privateBody,
        };
        await HTTP.post(path, JSON.stringify(data));
    }

    static async resourcelistAll(resourceUid) {
        App._verify(App._verifyUid(resourceUid));
        const path = `/resources/${resourceUid}/entries`;
        const [text, status] = await HTTP.get(path);
        return JSON.parse(text);
    }
}
