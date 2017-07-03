define(['pytsite-http-api'], function (httpApi) {
    function reload() {
        return httpApi.post('reload');
    }

    $('#pytsite-reload-link').click(function (e) {
        e.preventDefault();

        var link = $(this);
        if (confirm(t('pytsite.reload@confirm_application_reload'))) {
            reload().done(function () {
                link.parent().text(t('pytsite.reload@app_is_reloading'));
                setTimeout(function () {
                    location.reload();
                }, 5000)
            });
        }
    });

    return {
        reload: reload
    }
});