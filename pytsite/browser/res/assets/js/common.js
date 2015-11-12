var pytsite = {};

pytsite.js = {
    request: function(method, endpoint, data, success, error) {
        return $.ajax({
            url: '/pytsite/browser/' + endpoint,
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
