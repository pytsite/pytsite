$(function () {
    $('.widget-twitter-oauth').each(function () {
        var widget = $(this);
        var form = widget.closest('form');

        form.submit(function (e) {
            if (!widget.hasClass('hidden')) {
                widget.removeClass('has-error');
                widget.find('span.help-block.error').remove();
                var oauth_token = widget.find('input[name="' + widget.data('widgetUid') + '[oauth_token]"]').first().val();
                if (!oauth_token) {
                    var msg = t('pytsite.twitter@you_nas_not _authorized');
                    widget.addClass('has-error');
                    widget.append('<span class="help-block error">' + msg + '</span>');
                    return false;
                }
            }
        });
    });
});