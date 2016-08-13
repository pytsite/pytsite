pytsite.httpApi = {
    url: function (endpoint, data) {
        var version = $('meta[name="pytsite-http-api-version"]').attr('content');

        var url_prefix = '/';
        if (pytsite.lang.current() != pytsite.lang.fallback())
            url_prefix += pytsite.lang.current() + '/';

        var r = url_prefix + 'api/' + version + '/' + endpoint;
        if (data instanceof Object)
            r += '?' + $.param(data);

        return r;
    },

    request: function (method, endpoint, data) {
        data = data || {};
        data['__user_agent'] = navigator.userAgent;

        return $.ajax({
            url: pytsite.httpApi.url(endpoint),
            method: method,
            data: data
        });
    },

    get: function (endpoint, data) {
        return pytsite.httpApi.request('GET', endpoint, data)
    },

    post: function (endpoint, data) {
        return pytsite.httpApi.request('POST', endpoint, data)
    },

    put: function (endpoint, data) {
        return pytsite.httpApi.request('PUT', endpoint, data)
    },

    patch: function (endpoint, data) {
        return pytsite.httpApi.request('PATCH', endpoint, data)
    },

    delete: function (endpoint, data) {
        return pytsite.httpApi.request('DELETE', endpoint, data)
    }
};
