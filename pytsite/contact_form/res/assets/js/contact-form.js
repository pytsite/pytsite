$(function () {
    $(window).on('pytsite.form.submit', function (e, form) {
        if (form.cid == 'pytsite.contact_form._form.Form') {
            pytsite.ajax.post('pytsite.contact_form.ep.submit', form.serialize())
                .done(function (response) {
                    alert(response.message);
                    form.em[0].reset();
                })
                .fail(function () {
                    alert(t('pytsite.contact_form@error_occurred'));
                });
        }
    });
});