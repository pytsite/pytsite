pytsite.flag = {
    init: function () {
        $('.widget-flag:not(".initialized")').each(function () {
            var widget = $(this);
            var uid = widget.data('uid');

            widget.find('a').click(function (e) {
                e.preventDefault();

                pytsite.js.post('pytsite.flag.ep.toggle', {
                    uid: uid
                }, function (data) {
                    if (data['status'] == 'flagged')
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
