define(['jquery', 'assetman-build-timestamps'], function ($, tStamps) {
    function assetUrl(url) {
        if (url.indexOf('/') === 0 || url.indexOf('http') === 0)
            return url;

        var pkgName = $('meta[name="pytsite-theme"]').attr('content');
        var assetPath = url;
        var urlParts = url.split('@');

        if (urlParts.length === 2) {
            pkgName = urlParts[0];
            assetPath = urlParts[1];
        }

        return location.origin + '/assets/' + pkgName + '/' + assetPath + '?v=' + tStamps[pkgName];
    }

    function loadResource(resType, resLoc, callbackFunc, async) {
        resLoc = assetUrl(resLoc).replace(/\?v=[0-9a-f]+/, '');

        // Async is default for CSS but not for JS
        if (async === undefined)
            async = resType !== 'js';

        // Call self in async manner
        if (async === true) {
            var deferred = $.Deferred();

            setTimeout(function () {
                // It is important to pass 'false' as last argument!
                loadResource(resType, resLoc, callbackFunc, false);
                deferred.resolve();
            }, 0);

            return deferred;
        }

        switch (resType) {
            case 'css':
                if (!$('link[href^="' + resLoc + '"]').length)
                    $('head').append($('<link rel="stylesheet" href="' + resLoc + '">'));
                break;

            case 'js':
                if (!$('script[src^="' + resLoc + '"]').length)
                    $('body').append($('<script type="text/javascript" src="' + resLoc + '"></script>'));
                break;

            default:
                throw 'Unexpected resource type: ' + resType;
        }

        if (callbackFunc)
            callbackFunc(resLoc);
    }

    function loadJS(location, callback, async) {
        return loadResource('js', location, callback, async)
    }

    function loadCSS(location, callback, async) {
        return loadResource('css', location, callback, async)
    }

    function parseLocation(skipEmpty) {
        function split(s) {
            var r = {};

            s = s.split('&');
            for (var i = 0; i < s.length; ++i) {
                var part = s[i].split('=');
                if (part.length === 1 && part[0].length) {
                    r[decodeURIComponent(part[0])] = null;
                }
                else if (part.length === 2) {
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
                if (r[l] instanceof Array && r[l].length === 1)
                    r[l] = r[l][0];

                if (skipEmpty === true && !r[l])
                    delete r[l];
            }

            return r;
        }

        return {
            href: window.location.href,
            origin: window.location.origin,
            protocol: window.location.protocol,
            host: window.location.host,
            port: window.location.port,
            pathname: window.location.pathname,
            query: split(window.location.search.replace(/^\?/, '')),
            hash: split(window.location.hash.replace(/^#/, ''))
        };
    }

    function encodeQuery(data) {
        var r = [];
        for (var k in data) {
            if (data.hasOwnProperty(k)) {
                if (data.k instanceof Array) {
                    for (var l = 0; l < data.k.length; l++) {
                        r.push(encodeURIComponent(k) + "[]=" + encodeURIComponent(data[k][l]));
                    }
                }
                else {
                    r.push(encodeURIComponent(k) + "=" + encodeURIComponent(data[k]));
                }
            }
        }

        return r.join("&");
    }

    return {
        assetUrl: assetUrl,
        loadJS: loadJS,
        loadCSS: loadCSS,
        parseLocation: parseLocation,
        encodeQuery: encodeQuery
    }
});
