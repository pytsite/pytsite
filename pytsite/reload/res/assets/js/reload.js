require(['jquery', 'pytsite-reload', 'pytsite-lang'], function ($, reload, lang) {
    $('#pytsite-reload-link').click(function (e) {
        e.preventDefault();

        var link = $(this);
        if (confirm(lang.t('pytsite.reload@confirm_application_reload'))) {
            reload.reload().done(function () {
                link.parent().text(lang.t('pytsite.reload@app_is_reloading'));
                setTimeout(function () {
                    location.reload();
                }, 3000)
            });
        }
    });
});
