define(['assetman', 'pytsite-widget-input-string-list'], function(assetman, stringList) {
    assetman.loadCSS('pytsite.widget@css/list-list.css');

    return function(widget) {
        stringList(widget);
    }
});
