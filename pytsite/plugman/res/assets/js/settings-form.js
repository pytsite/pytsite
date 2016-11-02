$(function () {
    var form = $('.pytsite-form.setting-uid-plugman');

    form.on('pytsite.form.forward', function () {
        var actionBtn = form.find('.action-btn');

        actionBtn.click(function (e) {
            e.preventDefault();

            var btn = $(this);
            var icon = btn.find('i.fa');
            var endpoint = btn.attr('data-ep');
            var iconClass = icon.attr('class');

            btn.attr('disabled', true);
            icon.attr('class', 'fa fa-spin fa-spinner');

            pytsite.httpApi.post(endpoint, {name: btn.data('name')}).done(function () {
                // Wait some time while application finishes reloading
                setTimeout(function () {
                    location.reload();
                }, 5000);
            }).fail(function (r) {
                btn.attr('disabled', false);
                icon.attr('class', iconClass);

                if ('error' in r.responseJSON)
                    alert(r.responseJSON.error);
            });
        });
    });
});
