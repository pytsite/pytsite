pytsite.flag = {
    init: function () {
        $('.widget-flag:not(".initialized")').each(function () {
            var widget = $(this);
            var entity = widget.data('entity');

            widget.find('a').click(function (e) {
                e.preventDefault();

                pytsite.ajax.post('pytsite.flag.ep.toggle', {
                    entity: entity
                }, function (data) {
                    if (data['status'])
                        widget.addClass('flagged');
                    else
                        widget.removeClass('flagged');

                    widget.find('.count').text(data['count']);
                });
            });

            widget.addClass('initialized');
        });
    }
};

$(function () {
    pytsite.flag.init();
});
