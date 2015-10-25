$(function () {
    $('.widget-select-select2').each(function () {
        var theme = $(this).data('theme');
        var ajax_url = $(this).data('ajaxUrl');
        var ajax_delay = $(this).data('ajaxDelay');
        var ajax_data_type = $(this).data('ajaxDataType');

        $(this).find('select').select2({
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
});
