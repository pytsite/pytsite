$(function () {
    $('.widget-tumblr-oauth').each(function () {
        var widget = $(this);

        widget.find('select[name="driver_opts[user_blog]"]').change(function() {
            var screen_name = widget.find('input[name="driver_opts[screen_name]"]').first().val();
            widget.find('input[name="driver_opts[title]"]').val(screen_name + ' (' + $(this).val() + ')');
        });

        widget.closest('form').on('pytsite_form_submit', function (e, form) {
            if (!form.find('input[name="driver_opts[oauth_token]"]').val()) {
                alert(t('pytsite.tumblr@you_are_not_authorized'));
                form.removeClass('ready-to-submit');
            }
            else {
                form.addClass('ready-to-submit');
            }
        });
    });
});
