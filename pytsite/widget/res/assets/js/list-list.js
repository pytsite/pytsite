$(window).on('pytsite.widget.init:pytsite.widget._input.ListList', function (e, widget) {
    $(window).trigger('pytsite.widget.init:pytsite.widget._input.StringList', [widget]);
});
