$(window).on('pytsite.widget.init:pytsite.widget._input.Decimal', function (e, widget) {
    var options = {
        allowMinus: false
    };

    if (widget.data('allowMinus'))
        options.allowMinus = true;

    widget.find('input[type=text],input[type=tel],input[type=number]').inputmask('decimal', options);
});
