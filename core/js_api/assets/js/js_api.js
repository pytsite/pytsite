pytsite.js_api = {
    request: function(method, endpoint, data) {
        return $.ajax({
            url: '/pytsite/core/js_api/' + endpoint,
            method: method,
            data: data
        });
    },
    get: function(endpoint, data) {
        return pytsite.js_api.request('GET', endpoint, data)
    },
    post: function(endpoint, data) {
        return pytsite.js_api.request('POST', endpoint, data)
    }
};