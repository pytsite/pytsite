$(function () {
    $('.widget-vk-oauth').each(function () {
        var widget = $(this);
        var access_url_input = widget.find('#access_url');
        var access_token_input = widget.find('#access_token');
        var user_id_input = widget.find('#user_id');

        access_url_input.on('change', function () {
            var text = access_url_input.val();
            access_token_input.val(text.replace(/^.+access_token=([a-z0-9]{85}).+$/, '$1'));
            user_id_input.val(text.replace(/^.+user_id=(\d+)$/, '$1'));
        });

        widget.closest('form').on('pytsite_form_submit', function (e, form) {
            if (!access_token_input.val().match(/^[a-z0-9]+$/) || !user_id_input.val().match(/^\d+$/)) {
                alert(t('pytsite.vk@invalid_access_url'));
                form.removeClass('ready-to-submit');
            }
            else {
                form.addClass('ready-to-submit');
            }
        });
    });
});
