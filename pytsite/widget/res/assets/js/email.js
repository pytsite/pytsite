$(window).on('pytsite.widget.init:pytsite.widget._input.Email', function (e, widget) {
    $(window).trigger('pytsite.widget.init:pytsite.widget._input.Text', [widget]);
});
