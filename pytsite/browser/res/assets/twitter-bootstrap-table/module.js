define(['jquery', 'assetman', 'pytsite-lang'], function ($, assetman, lang) {
    assetman.loadCSS('pytsite.browser@twitter-bootstrap-table/bootstrap-table.css', null, false);
    assetman.loadJS('pytsite.browser@twitter-bootstrap-table/bootstrap-table.js', null, false);
    assetman.loadJS('pytsite.browser@twitter-bootstrap-table/locale/' + lang.current() + '.js', null, false);
    assetman.loadJS('pytsite.browser@twitter-bootstrap-table/extensions/cookie.js', null, false);
});
