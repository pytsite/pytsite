require(['jquery', 'pytsite-http-api', 'pytsite-lang'], function ($, httpApi, lang) {
    $('.pytsite-form.setting-uid-plugman').on('formForward', function (e, form) {
        var actionBtn = form.em.find('.action-btn');

        actionBtn.click(function (e) {
            e.preventDefault();

            var btn = $(this);
            var actionBtns = form.em.find('.action-btn');
            var icon = btn.find('i.fa');
            var endpoint = btn.attr('data-ep');
            var iconClass = icon.attr('class');

            switch (endpoint) {
                case 'plugman/install':
                    if (!confirm(lang.t('pytsite.plugman@confirm_plugin_install')))
                        return;
                    break;

                case 'plugman/upgrade':
                    if (!confirm(lang.t('pytsite.plugman@confirm_plugin_upgrade')))
                        return;
                    break;

                case 'plugman/uninstall':
                    if (!confirm(lang.t('pytsite.plugman@confirm_plugin_uninstall')))
                        return;
                    break;

                default:
                    return;
            }

            // Disable all action buttons
            actionBtns.attr('disabled', true);

            // Add spinner to the clicked button
            icon.attr('class', 'fa fa-spin fa-spinner');

            httpApi.post(endpoint + '/' + btn.data('name')).done(function () {
                // Wait some time while application finishes reloading
                setTimeout(function () {
                    location.reload();
                }, 5000);
            }).fail(function (r) {
                actionBtns.attr('disabled', false);
                icon.attr('class', iconClass);

                if ('error' in r.responseJSON)
                    alert(r.responseJSON.error);
            });
        });
    });
});

