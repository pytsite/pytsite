$(function () {
    $('.widget-tumblr-oauth').each(function () {
        var widget = $(this);
        var blog_select = widget.find('select[name="driver_opts[user_blog]"]');
        var screen_name = widget.find('input[name="driver_opts[screen_name]"]');
        var driver_title = widget.find('input[name="driver_opts[title]"]');

        driver_title.val(screen_name.val() + ' (' + blog_select.val() + ')');

        blog_select.change(function() {
            driver_title.val(screen_name.val() + ' (' + $(this).val() + ')');
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
