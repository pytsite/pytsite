define(['assetman', 'pytsite-lang', 'twitter-bootstrap-table-vendor'], function (assetman, lang) {
    assetman.loadCSS('pytsite.browser@twitter-bootstrap-table/bootstrap-table.css');
    assetman.loadJS('pytsite.browser@twitter-bootstrap-table/locale/' + lang.current() + '.js');
    assetman.loadJS('pytsite.browser@twitter-bootstrap-table/extensions/cookie.js');
});
