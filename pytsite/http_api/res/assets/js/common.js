pytsite.httpApi = {
    url: function (endpoint, data, version) {
        if (!version) {
            version = '1';
        }

        var url_prefix = '/';
        if (pytsite.lang.current() != pytsite.lang.fallback())
            url_prefix += pytsite.lang.current() + '/';

        var r = url_prefix + 'api/' + version + '/' + endpoint;
        if (data instanceof Object)
            r += '?' + $.param(data);

        return r;
    },

    request: function (method, endpoint, data, version) {
        data = data || {};
        data['__user_agent'] = navigator.userAgent;

        return $.ajax({
            url: pytsite.httpApi.url(endpoint, null, version),
            method: method,
            data: data
        });
    },

    get: function (endpoint, data, version) {
        return pytsite.httpApi.request('GET', endpoint, data, version)
    },

    post: function (endpoint, data, version) {
        return pytsite.httpApi.request('POST', endpoint, data, version)
    },

    put: function (endpoint, data, version) {
        return pytsite.httpApi.request('PUT', endpoint, data, version)
    },

    patch: function (endpoint, data, version) {
        return pytsite.httpApi.request('PATCH', endpoint, data, version)
    },

    delete: function (endpoint, data, version) {
        return pytsite.httpApi.request('DELETE', endpoint, data, version)
    }
};
