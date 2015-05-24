pytsite.js_api = {
    request: function(method, endpoint, data) {
        var r = response = $.ajax({
            url: '/pytsite/core/js_api/' + endpoint,
            async: false,
            method: method,
            data: data
        });

        return r.responseJSON;
    },
    get: function(endpoint, data) {
        return pytsite.js_api.request('GET', endpoint, data)
    },
    post: function(endpoint, data) {
        return pytsite.js_api.request('POST', endpoint, data)
    }
};