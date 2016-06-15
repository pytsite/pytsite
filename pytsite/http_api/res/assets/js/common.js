pytsite.httpApi = {
    url: function (endpoint, data) {
        var pkg = 'app';
        var callback = endpoint;
        var version = $('meta[name="pytsite-http-api-version"]').attr('content');

        var url_prefix = '/';
        if (pytsite.lang.current() != pytsite.lang.fallback())
            url_prefix += pytsite.lang.current() + '/';

        if (endpoint.indexOf('@') > 0) {
            var epSplit = endpoint.split('@');
            pkg = epSplit[0];
            callback = epSplit[1];
        }

        var r = url_prefix + 'api/' + version + '/' + pkg + '/' + callback;
        if (data instanceof Object)
            r += '?' + $.param(data);

        return r;
    },

    request: function (method, endpoint, data) {
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
    }
};
