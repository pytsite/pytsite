define(['jquery'], function ($) {
    return function (widget) {
        var switches = widget.em.find('.switch');
        var input = widget.em.find('input');

        switches.click(function (e) {
            e.preventDefault();
            if (widget.em.data('enabled') === 'True') {
                switches.removeClass('active');
                $(this).addClass('active');
                input.val($(this).data('score'));
            }
        });
    }
});
