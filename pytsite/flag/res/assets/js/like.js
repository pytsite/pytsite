$(window).on('pytsite.widget.init:pytsite.flag._widget.Like', function (e, widget) {
    widget.em.find('a').click(function (e) {
        e.preventDefault();

        var em = widget.em;

        if (widget.em.hasClass('flagged') && !confirm(t('pytsite.flag@dislike_confirmation')))
            return;

        pytsite.httpApi.patch('flag/toggle', {
            model: em.data('model'),
            uid: em.data('uid')
        }).done(function (data) {
            if (data['status']) {
                em.addClass('flagged');
                em.find('a').attr('title', t('pytsite.flag@dislike'));
            }
            else {
                em.removeClass('flagged');
                em.find('a').attr('title', t('pytsite.flag@like'));
            }

            em.find('.count').text(data['count']);
        });
    });
});
