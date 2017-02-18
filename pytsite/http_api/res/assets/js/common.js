pytsite.httpApi = {
    url: function (endpoint, data, version) {
        if (typeof version === 'undefined' || version == null) {
            version = '1';
        }

        var r = '/api/' + version + '/' + endpoint;
        if (data instanceof Object)
            r += '?' + $.param(data);

        return r;
    },

    request: function (method, endpoint, data, version, includeUA) {
        data = data || {};

        if (typeof includeUA === 'undefined' || includeUA == true)
            data['__user_agent'] = navigator.userAgent;

        return $.ajax({
            url: pytsite.httpApi.url(endpoint, null, version),
            method: method,
            data: data
        });
    },

    get: function (endpoint, data, version, includeUA) {
        return pytsite.httpApi.request('GET', endpoint, data, version, includeUA)
    },

    post: function (endpoint, data, version, includeUA) {
        return pytsite.httpApi.request('POST', endpoint, data, version, includeUA)
    },

    put: function (endpoint, data, version, includeUA) {
        return pytsite.httpApi.request('PUT', endpoint, data, version, includeUA)
    },

    patch: function (endpoint, data, version, includeUA) {
        return pytsite.httpApi.request('PATCH', endpoint, data, version, includeUA)
    },

    delete: function (endpoint, data, version, includeUA) {
        return pytsite.httpApi.request('DELETE', endpoint, data, version, includeUA)
    }
};
