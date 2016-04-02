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
        if (loc instanceof String)
            loc = [loc];

        for (var i = 0; i < loc.length; i++) {
            if (loc[i] instanceof String) {
                if (loc[i].indexOf('.js') > 0)
                    pytsite.browser.addJS(loc[i]);
                else if (loc[i].indexOf('.css') > 0)
                    pytsite.browser.addCSS(loc[i]);
                else
                    throw "Cannot determine type of the asset '{0}'.".format(loc[i]);
            }
            else if (loc[i] instanceof Array) {
                if (loc[i][1] == 'js')
                    pytsite.browser.addJS(loc[i][0]);
                else if (loc[i][1] == 'css')
                    pytsite.browser.addCSS(loc[i][0]);
                else
                    throw "Cannot determine type of the asset '{0}'.".format(loc[i][0]);
            }
        }
    },

    addJS: function (loc) {
        loc = pytsite.browser.assetUrl(loc);
        if (!$('script[src="' + loc + '"]').length)
            $('body').append($('<script type="text/javascript" src="' + loc + '"></script>'));
    },

    addCSS: function (loc) {
        loc = pytsite.browser.assetUrl(loc);
        if (!$('link[href="' + loc + '"]').length)
            $('head').append($('<link rel="stylesheet" href="' + loc + '">'));
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

