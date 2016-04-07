$(window).on('pytsite.widget.init:pytsite.widget._input.Text', function (e, widget) {
    widget.em.find('input').focus(function () {
        this.select();
    });
});
