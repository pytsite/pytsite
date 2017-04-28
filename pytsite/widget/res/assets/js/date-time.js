define(['pytsite-lang', 'jquery-date-time-picker'], function (lang) {
    return function (widget) {
        widget.em.find('input').datetimepicker({
            lang: lang.current(),
            format: 'd.m.Y H:i',
            defaultDate: new Date()
        });
    }
});
