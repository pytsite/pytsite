$(function() {
    $('.widget-input-text').each(function() {
        var widget = $(this);
        var input = widget.find('input');

        input.focus(function() {
            this.select();
        });
    });
});