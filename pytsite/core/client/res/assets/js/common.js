pytsite = {};

pytsite.js = {
    request: function(method, endpoint, data, success, error) {
        return $.ajax({
            url: '/core/js/' + endpoint,
            method: method,
            data: data,
            success: success,
            error: error
        });
    },
    get: function(endpoint, data, success, error) {
        return pytsite.js.request('GET', endpoint, data, success, error)
    },
    post: function(endpoint, data, success, error) {
        return pytsite.js.request('POST', endpoint, data, success, error)
    }
};
