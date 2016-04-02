$(window).on('pytsite.widget.init:pytsite.wallet._widget.MoneyInput', function (e, widget) {
    // Redirect event to Decimal widget
    $(window).trigger('pytsite.widget.init:pytsite.widget._input.Decimal', [widget]);
});