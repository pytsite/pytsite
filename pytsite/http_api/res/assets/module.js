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

    function request(method, endpoint, data, version, includeUA) {
        data = data || {};

        if (typeof includeUA === 'undefined' || includeUA === true)
            data['__user_agent'] = navigator.userAgent;

        return $.ajax({
            url: url(endpoint, null, version),
            method: method,
            data: data,
            headers: {'PytSite-Lang': lang.current()}
        });
    }

    function get(endpoint, data, version, includeUA) {
        return request('GET', endpoint, data, version, includeUA)
    }

    function post(endpoint, data, version, includeUA) {
        return request('POST', endpoint, data, version, includeUA)
    }

    function put(endpoint, data, version, includeUA) {
        return request('PUT', endpoint, data, version, includeUA)
    }

    function patch(endpoint, data, version, includeUA) {
        return request('PATCH', endpoint, data, version, includeUA)
    }

    function del(endpoint, data, version, includeUA) {
        return request('DELETE', endpoint, data, version, includeUA)
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
