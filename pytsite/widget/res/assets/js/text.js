$(window).on('pytsite.widget.init:pytsite.widget._input.Text', function (e, widget) {
    widget.find('input').focus(function () {
        this.select();
    });
});
