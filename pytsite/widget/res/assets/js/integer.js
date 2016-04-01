$(window).on('pytsite.widget.init', function (e, widget) {
    widget.em.find('.widget-input-integer').each(function () {
        var options = {
            allowMinus: false
        };

        if ($(this).data('allowMinus'))
            options.allowMinus = true;

        $(this).find('input[type=text],input[type=tel],input[type=number]').inputmask('integer', options);
    });
});
