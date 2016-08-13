$(function () {
    $(window).on('pytsite.form.submit', function (e, form) {
        if (form.cid == 'pytsite.contact_form._form.Form') {
            pytsite.httpApi.post('contact_form/submit', form.serialize())
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
