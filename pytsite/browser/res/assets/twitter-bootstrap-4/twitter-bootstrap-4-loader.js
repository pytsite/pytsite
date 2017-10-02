define(['assetman', 'popper'], function(assetman, popper) {
    window.Popper = popper;
    assetman.loadCSS('pytsite.browser@twitter-bootstrap-4/css/bootstrap.css');
    assetman.loadJS('pytsite.browser@twitter-bootstrap-4/js/bootstrap.js');
});

