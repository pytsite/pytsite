define(['pytsite-lang', 'select2'], function (lang) {
    return function (widget) {
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
                    data['results'].unshift({id: '', text: '--- ' + lang.t('pytsite.widget@select_none_item') + ' ---'});
                    return data;
                }
            }
        });
    }
});
