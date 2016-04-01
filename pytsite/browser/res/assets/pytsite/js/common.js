if (!String.prototype.format) {
    String.prototype.format = function () {
        var args = arguments;
        return this.replace(/{(\d+)}/g, function (match, number) {
            return typeof args[number] != 'undefined' ? args[number] : match;
        });
    };
}

var pytsite = {};

pytsite.browser = {
    assetUrl: function (url) {
        if (url.indexOf('/') == 0 || url.indexOf('http') == 0)
            return url;

        var pkgName = 'app';
        var assetPath = url;
        var urlParts = url.split('@');

        if (urlParts.length == 2) {
            pkgName = urlParts[0];
            assetPath = urlParts[1];
        }

        return '/assets/{0}/{1}'.format(pkgName, assetPath);
    },

    addAssets: function (loc) {
        if (typeof loc == 'string')
            loc = [loc];

        for (var i = 0; i < loc.length; i++) {
            if (loc[i].indexOf('.js') > 0)
                pytsite.browser.addJS(loc[i]);
            else if (loc[i].indexOf('.css') > 0)
                pytsite.browser.addCSS(loc[i]);
            else
                throw "Cannot determine type of the asset '{0}'.".format(loc[i]);
        }
    },

    addJS: function (loc) {
        if (typeof loc == 'string')
            loc = [loc];

        for (var i = 0; i < loc.length; i++) {
            loc[i] = pytsite.browser.assetUrl(loc[i]);
            if (!$('script[src="' + loc[i] + '"]').length)
                $('body').append($('<script type="text/javascript" src="' + loc[i] + '"></script>'));
        }
    },

    addCSS: function (loc) {
        if (typeof loc == 'string')
            loc = [loc];

        for (var i = 0; i < loc.length; i++) {
            loc[i] = pytsite.browser.assetUrl(loc[i]);
            if (!$('link[href="' + loc[i] + '"]').length)
                $('head').append($('<link rel="stylesheet" href="' + loc[i] + '">'));
        }
    },

    getLocationHash: function () {
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

