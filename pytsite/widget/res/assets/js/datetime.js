$(function() {
    $('.widget-select-datetime').each(function() {
        var widget = $(this);
        widget.find('input').datetimepicker({
            lang: pytsite.lang.current,
            format: 'd.m.Y H:i',
            defaultDate: new Date()
        });
    });
});