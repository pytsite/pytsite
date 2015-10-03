$(function () {
    $('#pytsite-contact-form').on('pytsite_form_submit', function (e, form) {
        form.removeClass('ready-to-submit');

        pytsite.js.post('pytsite.contact.ep.submit', form.serializeForm(), function(response) {
            alert(response);
            form[0].reset();
        }, function() {
            alert(t('pytsite.contact@error_occurred'));
        });
    });
});
