$(function() {
    $('.widget-flag').each(function() {
        var widget = $(this);
        var uid = widget.data('uid');

        widget.find('a').click(function(e) {
            e.preventDefault();

            pytsite.js.post('pytsite.flag.eps.toggle', {
                uid: uid
            }, function(data) {
                if(data['status'] == 'flagged')
                    widget.addClass('flagged');
                else
                    widget.removeClass('flagged');

                widget.find('.count').text(data['count']);
            });
        });
    });
});