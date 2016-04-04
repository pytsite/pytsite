$(window).on('pytsite.widget.init:pytsite.taxonomy._widget.TokensInput', function (e, widget) {
    $(window).trigger('pytsite.widget.init:pytsite.widget._input.Tokens', [widget]);
});
