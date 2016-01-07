$(function() {
    $('.widget-content-export-lj-settings').each(function() {
        var widget = $(this);

        widget.find('#username').change(function() {
            widget.find('#title').val($(this).val());
        });
    });
});
