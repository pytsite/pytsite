pytsite.ajax = {
    // Constructs URL of AJAX endpoint
    url: function (endpoint, data) {
        var url_prefix = '/';
        if (pytsite.lang.current() != pytsite.lang.fallback())
            url_prefix += pytsite.lang.current() + '/';

        var r = url_prefix + 'pytsite/ajax/' + endpoint;
        if (data instanceof Object)
            r += '?' + $.param(data);

        return r;
    },

    request: function (method, endpoint, data) {
        return $.ajax({
            url: pytsite.ajax.url(endpoint),
            method: method,
            data: data
        });
    },

    get: function (endpoint, data) {
        return pytsite.ajax.request('GET', endpoint, data)
    },

    post: function (endpoint, data) {
        return pytsite.ajax.request('POST', endpoint, data)
    }
};
