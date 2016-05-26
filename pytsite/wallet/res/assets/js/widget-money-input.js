$(window).on('pytsite.widget.init:pytsite.wallet._widget.MoneyInput', function (e, widget) {
    widget.em.find('input[type=text],input[type=tel],input[type=number]').inputmask('decimal', {
        allowMinus: false
    });

    $(window).trigger('pytsite.widget.init:pytsite.widget._input.Text', [widget]);
});
