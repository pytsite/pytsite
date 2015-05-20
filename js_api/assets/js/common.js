pytsite.js_api = {
    request: function(method, endpoint, arg) {
        $.ajax({
            async: false,
            method: method
        })
    },
    get: function(endpoint, args) {
        pytsite.js_api.request('GET', endpoint, args)
    },
    post: function(endpoint, args) {
        pytsite.js_api.request('POST', endpoint, args)
    }
};