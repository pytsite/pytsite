pytsite.js_api = {
    request: function(method, endpoint, data) {
        var response = $.ajax({
            url: '/js_api/' + endpoint,
            async: false,
            method: method,
            data: data
        })
    },
    get: function(endpoint, data) {
        return pytsite.js_api.request('GET', endpoint, data)
    },
    post: function(endpoint, data) {
        return pytsite.js_api.request('POST', endpoint, data)
    }
};