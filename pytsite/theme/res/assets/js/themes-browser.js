define(['pytsite-lang', 'pytsite-http-api'], function (lang, httpApi) {
    return function (widget) {
        widget.em.find('.button-switch').click(function() {
            if (confirm(lang.t('pytsite.theme@theme_switch_confirmation'))) {
                $(this).closest('table').find('.btn').addClass('disabled');
                $(this).find('i').removeClass().addClass('fa fa-spin fa-spinner');

                var rData = {package_name: $(this).data('packageName')};
                httpApi.patch(widget.data('httpApiEpSwitch'), rData).always(function() {
                    setTimeout(function() {
                        location.reload();
                    }, 1000)
                });
            }
        });

        widget.em.find('.button-uninstall').click(function() {
            if (confirm(lang.t('pytsite.theme@theme_uninstall_confirmation'))) {
                $(this).closest('table').find('.btn').addClass('disabled');
                $(this).find('i').removeClass().addClass('fa fa-spin fa-spinner');

                var rData = {package_name: $(this).data('packageName')};
                httpApi.del(widget.data('httpApiEpUninstall'), rData).always(function() {
                    setTimeout(function() {
                        location.reload();
                    }, 1000)
                });
            }
        });
    }
});
