$(window).on('pytsite.widget.init:pytsite.widget._select.Select2', function (e, widget) {
    var theme = widget.em.data('theme');
    var ajax_url = widget.em.data('ajaxUrl');
    var ajax_delay = widget.em.data('ajaxDelay');
    var ajax_data_type = widget.em.data('ajaxDataType');

    widget.em.find('select').select2({
        theme: theme,
        ajax: {
            url: ajax_url,
            delay: ajax_delay,
            dataType: ajax_data_type,
            processResults: function (data) {
                data['results'].unshift({id: '', text: '--- ' + t('pytsite.widget@select_none_item') + ' ---'});
                return data;
            }
        }
    });
});
