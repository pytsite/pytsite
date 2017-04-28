$('.settings-form').on('formForward', function (e, form) {
    var themeSelect = form.em.find('select[name=setting_default_theme]');

    themeSelect.change(function () {
        $.each(form.widgets, function (i, widget) {
            if (widget.uid.indexOf('setting_theme_') == 0) {
                form.removeWidget(widget.uid);
            }
        });

        var themeName = $(this).val();
        if (!themeName)
            return;

        pytsite.httpApi.get('theme/settings/' + themeName).done(function (r) {
            $.each(r, function (i, widgetData) {
                form.createWidget(widgetData).done(function (widget) {
                    form.addWidget(widget);
                    widget.show();
                });
            });
        });
    });

    themeSelect.change();
});
