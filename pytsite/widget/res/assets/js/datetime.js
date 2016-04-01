$(window).on('pytsite.widget.init', function (e, widget) {
    widget.em.find('.widget-select-datetime input').each(function () {
        $(this).datetimepicker({
            lang: pytsite.lang.current(),
            format: 'd.m.Y H:i',
            defaultDate: new Date()
        });
    });
});
