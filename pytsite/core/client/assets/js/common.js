pytsite = {};

pytsite.js = {
    request: function(method, endpoint, data) {
        return $.ajax({
            url: '/core/js/' + endpoint,
            method: method,
            data: data
        });
    },
    get: function(endpoint, data) {
        return pytsite.js.request('GET', endpoint, data)
    },
    post: function(endpoint, data) {
        return pytsite.js.request('POST', endpoint, data)
    }
};
