$(function () {
    var widget = $('.widget-auth-ui-follow');

    widget.mouseover(function () {
        var btn = $(this).find('.btn');
        if (btn.hasClass('following')) {
            btn.removeClass('btn-primary').addClass('btn-danger');
            btn.find('.icon').removeClass('fa-check').addClass('fa-remove');
            btn.find('.text').text(t('pytsite.auth_ui@unfollow'));
        }
    });

    widget.mouseout(function () {
        var btn = $(this).find('.btn');
        if (btn.hasClass('following')) {
            btn.removeClass('btn-danger').addClass('btn-primary');
            btn.find('.icon').removeClass('fa-remove').addClass('fa-check');
            btn.find('.text').text(t('pytsite.auth_ui@following'));
        }
    });
    
    widget.click(function() {
        var btn = $(this).find('.btn');
        if (btn.hasClass('following')) {
            pytsite.js.post('pytsite.auth_ui.ep.follow', {op: 'unfollow', uid: widget.data('uid')}, function(data) {
                if (typeof data.status != 'undefined' && data.status === true) {
                    btn.removeClass('btn-danger').addClass('btn-default').removeClass('following').addClass('non-following');
                    btn.find('.icon').addClass('fa-plus');
                    btn.find('.text').text(t('pytsite.auth_ui@follow'));
                }
            });
        }
        else if (btn.hasClass('non-following')) {
            pytsite.js.post('pytsite.auth_ui.ep.follow', {op: 'follow', uid: widget.data('uid')}, function(data) {
                if (typeof data.status != 'undefined' && data.status === true) {
                    btn.removeClass('btn-default').addClass('btn-danger').removeClass('non-following').addClass('following');
                    btn.find('.icon').removeClass('fa-plus').addClass('fa-remove');
                    btn.find('.text').text(t('pytsite.auth_ui@unfollow'));
                }
            });
        }
    });
});
