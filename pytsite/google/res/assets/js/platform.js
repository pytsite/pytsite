pytsite.google.platform = {
    ready: false
};

window.pytsiteGooglePlatformInitCallback = function () {
    pytsite.google.platform.ready = true;
    $(window).trigger('pytsite.google.platform.ready');
};
