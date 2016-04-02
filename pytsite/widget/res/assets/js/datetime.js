$(window).on('pytsite.widget.init:pytsite.widget._select.DateTime', function (e, widget) {
    widget.find('input').datetimepicker({
        lang: pytsite.lang.current(),
        format: 'd.m.Y H:i',
        defaultDate: new Date()
    });
});
