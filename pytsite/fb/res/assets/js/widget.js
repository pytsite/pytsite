$(function () {
    $('.widget-fb-oauth').each(function () {
        var widget = $(this);
        var page_select = widget.find('select[name="driver_opts[page_id]"]');
        var screen_name = widget.find('input[name="driver_opts[screen_name]"]');
        var driver_title = widget.find('input[name="driver_opts[title]"]');

        if (page_select.val())
            driver_title.val(screen_name.val() + ' (' + page_select.find('option:selected').text() + ')');

        page_select.change(function() {
            if (page_select.val())
                driver_title.val(screen_name.val() + ' (' + page_select.find('option:selected').text() + ')');
            else
                driver_title.val(screen_name.val());
        });

        widget.closest('form').on('pytsite_form_submit', function (e, form) {
            if (!form.find('input[name="driver_opts[access_token]"]').val()) {
                alert(t('pytsite.fb@you_are_not_authorized'));
                form.removeClass('ready-to-submit');
            }
            else {
                form.addClass('ready-to-submit');
            }
        });
    });
});
