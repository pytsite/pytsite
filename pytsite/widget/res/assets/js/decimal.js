define(['jquery-inputmask', 'pytsite-widget-input-text'], function () {
    return function (widget) {
        var options = {
            allowMinus: false
        };

        if (widget.em.data('allowMinus'))
            options.allowMinus = true;

        widget.em.find('input[type=text],input[type=tel],input[type=number]').inputmask('decimal', options);
    }
});
