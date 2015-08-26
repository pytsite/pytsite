$(function () {
    $('.widget-input-float').each(function () {
        var widget = $(this);
        var options = {
            allowMinus: false
        };

        if(widget.data('allowMinus'))
            options.allowMinus = true;

        widget.find('input[type=text],input[type=tel]').inputmask('decimal', options);
    });
});