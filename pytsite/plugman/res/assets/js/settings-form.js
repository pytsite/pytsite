$(function () {
    var form = $('.pytsite-form.setting-uid-plugman');

    form.on('pytsite.form.forward', function () {
        var actionBtn = form.find('.action-btn');

        actionBtn.click(function (e) {
            e.preventDefault();

            var btn = $(this);
            var actionBtns = form.find('.action-btn');
            var icon = btn.find('i.fa');
            var endpoint = btn.attr('data-ep');
            var iconClass = icon.attr('class');

            if (endpoint.indexOf('upgrade') >= 0 && !confirm(t('pytsite.plugman@confirm_plugin_upgrade')))
                return;
            else if (endpoint.indexOf('uninstall') >= 0 && !confirm(t('pytsite.plugman@confirm_plugin_uninstall')))
                return;

            // Disable all action buttons
            actionBtns.attr('disabled', true);

            // Add spinner to the clicked button
            icon.attr('class', 'fa fa-spin fa-spinner');

            pytsite.httpApi.post(endpoint, {name: btn.data('name')}).done(function () {
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
