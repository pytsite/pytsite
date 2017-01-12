$(function () {
    $('#settings-form').on('pytsite.form.forward', function (e, form) {
        var themeSelect = form.em.find('select[name=setting_default_theme]');

        themeSelect.change(function (e) {
            $.each(form.widgets, function (i, widget) {
                if (widget.uid.indexOf('setting_theme_') == 0) {
                    form.removeWidget(widget.uid);
                }
            });

            var themeName = $(this).val();
            if (!themeName)
                return;

            pytsite.httpApi.get('theme/settings_widgets', {theme: themeName}).done(function (r) {
                $.each(r, function (i, widgetData) {
                    form.initWidget(widgetData).done(function(widget) {
                        form.addWidget(widget);
                        widget.show();
                    });
                });
            });
        });

        themeSelect.change();
    });
});