define(['jquery', 'pytsite-lang'], function ($, lang) {
    function url(endpoint, data, version) {
        if (typeof version === 'undefined' || version === null) {
            version = '1';
        }

        var r = '/api/' + version + '/' + endpoint;
        if (data instanceof Object)
            r += '?' + $.param(data);

        return r;
    }

    function request(method, endpoint, data, version) {
        data = data || {};

        return $.ajax({
            url: url(endpoint, null, version),
            method: method,
            data: data,
            headers: {'PytSite-Lang': lang.current()}
        });
    }

    function get(endpoint, data, version) {
        return request('GET', endpoint, data, version)
    }

    function post(endpoint, data, version) {
        return request('POST', endpoint, data, version)
    }

    function put(endpoint, data, version) {
        return request('PUT', endpoint, data, version)
    }

    function patch(endpoint, data, version) {
        return request('PATCH', endpoint, data, version)
    }

    function del(endpoint, data, version) {
        return request('DELETE', endpoint, data, version)
    }

    return {
        url: url,
        request: request,
        get: get,
        post: post,
        put: put,
        patch: patch,
        del: del
    }
});
