define(['jquery', 'assetman', 'pytsite-lang'], function ($, assetman, lang) {
    assetman.loadCSS('pytsite.browser@twitter-bootstrap-table/bootstrap-table.css');
    assetman.loadJS('pytsite.browser@twitter-bootstrap-table/bootstrap-table.js');
    assetman.loadJS('pytsite.browser@twitter-bootstrap-table/locale/' + lang.current() + '.js');
    assetman.loadJS('pytsite.browser@twitter-bootstrap-table/extensions/cookie.js');
});
