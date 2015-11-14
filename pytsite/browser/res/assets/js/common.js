var pytsite = {};

pytsite.browser = {
    request: function(method, endpoint, data, success, error) {
        var url_prefix = '/';
        if (pytsite.lang.current() != pytsite.lang.fallback())
            url_prefix += pytsite.lang.current() + '/';

        return $.ajax({
            url: url_prefix + 'pytsite/browser/' + endpoint,
            method: method,
            data: data,
            success: success,
            error: error
        });
    },

    get: function(endpoint, data, success, error) {
        return this.request('GET', endpoint, data, success, error)
    },

    post: function(endpoint, data, success, error) {
        return this.request('POST', endpoint, data, success, error)
    }
};
