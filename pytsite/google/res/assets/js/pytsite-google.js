pytsite.google = {
    ready: false,

    initCallback: function() {
        $(window).trigger('pytsite.google.ready');
        pytsite.google.ready = true;
    }
};
