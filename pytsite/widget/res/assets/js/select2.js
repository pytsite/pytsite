$(window).on('pytsite.widget.init:pytsite.widget._select.Select2', function (e, widget) {
    var theme = widget.data('theme');
    var ajax_url = widget.data('ajaxUrl');
    var ajax_delay = widget.data('ajaxDelay');
    var ajax_data_type = widget.data('ajaxDataType');

    widget.find('select').select2({
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
