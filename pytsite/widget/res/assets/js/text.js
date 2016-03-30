$(window).on('pytsite.widget.init', function (e, widget) {
    widget.em.find('.widget-input-text input').each(function () {
        $(this).focus(function () {
            this.select();
        });
    });
});
