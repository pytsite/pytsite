if (!String.prototype.format) {
    String.prototype.format = function () {
        var args = arguments;
        return this.replace(/{(\d+)}/g, function (match, number) {
            return typeof args[number] != 'undefined'
                ? args[number]
                : match
                ;
        });
    };
}

var pytsite = {};

pytsite.browser = {
    addJS: function(url) {
        if (!$('script[src="' + url + '"]').length)
            $('body').append($('<script type="text/javascript" src="' + url + '"></script>'));
    },

    addCSS: function(url) {
        if (!$('link[href="' + url + '"]').length)
            $('head').append($('<link rel="stylesheet" href="' + url + '">'));
    },

    getLocationHash: function() {
        var hash = window.location.hash.replace(/^#/, '').split('&');
        var r = {};
        for (var i = 0; i < hash.length; ++i) {
            var part = hash[i].split('=');
            if (part.length == 1) {
                r[decodeURIComponent(part[0])] = null;
            }
            else if (part.length == 2) {
                r[decodeURIComponent(part[0])] = decodeURIComponent(part[1]);
            }
        }

        return r
    }
};

