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

    request: function (method, endpoint, data, success, error) {
        return $.ajax({
            url: pytsite.ajax.url(endpoint),
            method: method,
            data: data,
            success: function (resp) {
                if (resp instanceof Object) {
                    if ('_css' in resp) {
                        $.each(resp['_css'], function (i, url) {
                            pytsite.browser.addCSS(url);
                        });

                        delete resp['_css'];
                    }

                    if ('_js' in resp) {
                        $.each(resp['_js'], function (i, url) {
                            pytsite.browser.addJS(url);
                        });

                        delete resp['_js'];
                    }

                    if (Object.keys(resp).length == 1)
                        resp = resp[Object.keys(resp)[0]];
                }

                if (success)
                    success(resp);
            },
            error: error
        });
    },

    get: function (endpoint, data, success, error) {
        return this.request('GET', endpoint, data, success, error)
    },

    post: function (endpoint, data, success, error) {
        return this.request('POST', endpoint, data, success, error)
    }
};
