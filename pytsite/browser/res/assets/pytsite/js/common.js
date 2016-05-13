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

        return location.origin + '/assets/{0}/{1}'.format(pkgName, assetPath);
    },

    loadAssets: function (loc) {
        var defer = $.Deferred();

        setTimeout(function () {
            if (loc instanceof String)
                loc = [loc];

            if (loc.length) {
                for (var i = 0; i < loc.length; i++) {
                    var assetSrc, assetType;

                    if (typeof loc[i] == 'string') {
                        assetSrc = loc[i];
                        if (loc[i].indexOf('.js') > 0)
                            assetType = 'js';
                        else if (loc[i].indexOf('.css') > 0)
                            assetType = 'css';
                    }
                    else if (loc[i] instanceof Array) {
                        assetSrc = loc[i][0];
                        if (loc[i][1] == 'js')
                            assetType = 'js';
                        else if (loc[i][1] == 'css')
                            assetType = 'css';
                    }

                    switch (assetType) {
                        case 'js':
                            pytsite.browser.addJS(assetSrc, i)
                                .done(function (index) {
                                    if (index + 1 == loc.length)
                                        defer.resolve();
                                });
                            break;

                        case 'css':
                            pytsite.browser.addCSS(assetSrc, i)
                                .done(function (index) {
                                    if (index + 1 == loc.length)
                                        defer.resolve();
                                });
                            break;

                        default:
                            defer.reject();
                            throw "Cannot determine type of the asset '{0}'.".format(assetSrc);
                    }
                }
            }
            else {
                defer.resolve();
            }
        }, 0);

        return defer;
    },

    addJS: function (loc, index) {
        var deffer = $.Deferred();

        setTimeout(function () {
            loc = pytsite.browser.assetUrl(loc);
            if (!$('script[src="' + loc + '"]').length) {
                $.ajaxSetup({cache: true});
                $('body').append($('<script type="text/javascript" src="' + loc + '"></script>'));
                $.ajaxSetup({cache: false});
            }

            deffer.resolve(index);
        }, 0);

        return deffer;
    },

    addCSS: function (loc, index) {
        var deffer = $.Deferred();

        setTimeout(function () {
            loc = pytsite.browser.assetUrl(loc);
            if (!$('link[href="' + loc + '"]').length) {
                $('head').append($('<link rel="stylesheet" href="' + loc + '">'));

            }

            deffer.resolve(index);
        }, 0);

        return deffer;
    },

    parseLocation: function (skipEmpty) {
        function split(s) {
            var r = {};

            s = s.split('&');
            for (var i = 0; i < s.length; ++i) {
                var part = s[i].split('=');
                if (part.length == 1 && part[0].length) {
                    r[decodeURIComponent(part[0])] = null;
                }
                else if (part.length == 2) {
                    var k = decodeURIComponent(part[0].replace('+', '%20'));
                    var v = decodeURIComponent(part[1].replace('+', '%20'));

                    if (k.indexOf('[]') > 0) {
                        k = k.replace('[]', '');

                        if (k in r && !(r[k] instanceof Array))
                            r[k] = [r[k]];
                        else
                            r[k] = [];

                        r[k].push(v);
                    }
                    else {
                        r[k] = v;
                    }
                }
            }

            for (var l in r) {
                if (r[l] instanceof Array && r[l].length == 1)
                    r[l] = r[l][0];

                if (skipEmpty == true && !r[l])
                    delete r[l];
            }

            return r;
        }

        return {
            query: split(window.location.search.replace(/^\?/, '')),
            hash: split(window.location.hash.replace(/^#/, ''))
        };
    },

    encodeQuery: function (data) {
        var r = [];
        for (var k in data) {
            if (data[k] instanceof Array) {
                for (var l = 0; l < data[k].length; l++) {
                    r.push(encodeURIComponent(k) + "[]=" + encodeURIComponent(data[k][l]));
                }
            }
            else {
                r.push(encodeURIComponent(k) + "=" + encodeURIComponent(data[k]));
            }
        }

        return r.join("&");
    }
};

