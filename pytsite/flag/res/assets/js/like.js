$(window).on('pytsite.widget.init:pytsite.flag._widget.Like', function (e, widget) {
    widget.em.find('a').click(function (e) {
        e.preventDefault();

        if (widget.em.hasClass('flagged') && !confirm(t('pytsite.flag@dislike_confirmation')))
            return;

        pytsite.ajax.post('pytsite.flag.ajax.like', {
                entity: widget.em.data('entity')
            })
            .done(function (data) {
                if (data['status']) {
                    widget.em.addClass('flagged');
                    widget.em.find('a').attr('title', t('pytsite.flag@dislike'));
                }

                else {
                    widget.em.removeClass('flagged');
                    widget.em.find('a').attr('title', t('pytsite.flag@like'));
                }

                widget.em.find('.count').text(data['count']);
            });
    });
});
