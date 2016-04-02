$(window).on('pytsite.widget.init:pytsite.image._widget.ImagesUpload', function (e, widget) {
    // Redirect event to FilesUpload widget
    $(window).trigger('pytsite.widget.init:pytsite.file._widget.FilesUpload', [widget]);
});