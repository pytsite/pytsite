pytsite.jsApi = {
    // Constructs URL of AJAX endpoint
    url: function (endpoint, data) {
        var url_prefix = '/';
        if (pytsite.lang.current() != pytsite.lang.fallback())
            url_prefix += pytsite.lang.current() + '/';

        var r = url_prefix + 'pytsite/js_api/' + endpoint;
        if (data instanceof Object)
            r += '?' + $.param(data);

        return r;
    },

    request: function (method, endpoint, data) {
        return $.ajax({
            url: pytsite.jsApi.url(endpoint),
            method: method,
            data: data
        });
    },

    get: function (endpoint, data) {
        return pytsite.jsApi.request('GET', endpoint, data)
    },

    post: function (endpoint, data) {
        return pytsite.jsApi.request('POST', endpoint, data)
    }
};
