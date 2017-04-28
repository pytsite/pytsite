define(['select2-main', 'assetman', 'pytsite-lang'], function(select2, assetman, lang) {
    assetman.loadCSS('pytsite.browser@select2/select2.css');
    assetman.loadCSS('pytsite.browser@select2/select2-bootstrap.css');
    assetman.loadJS('pytsite.browser@select2/i18n/' + lang.current() + '.js');

    return select2;
});
