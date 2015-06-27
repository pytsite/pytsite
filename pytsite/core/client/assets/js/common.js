pytsite = {};

pytsite.js = {
    request: function(method, endpoint, data, success) {
        return $.ajax({
            url: '/core/js/' + endpoint,
            method: method,
            data: data,
            success: success
        });
    },
    get: function(endpoint, data, success) {
        return pytsite.js.request('GET', endpoint, data, success)
    },
    post: function(endpoint, data, success) {
        return pytsite.js.request('POST', endpoint, data, success)
    }
};
