$.fn.serializeForm = function () {
    var o = {};
    var a = this.serializeArray();

    $.each(a, function () {
        if (o[this.name] !== undefined) {
            if (!o[this.name].push)
                o[this.name] = [o[this.name]];

            o[this.name].push(this.value || '');
        }
        else
            o[this.name] = this.value || '';
    });

    return o;
};

$(function () {
    $('.pytsite-form').each(function () {
        var form = $(this);

        form.submit(function (e) {
            // Detect validation endpoint and check if the form is already validated
            var validation_ep = form.data('validationEp');
            if (typeof validation_ep == 'undefined' || form.hasClass('validated')) {
                // If form doesn't define validation endpoint it considered as validated
                if (typeof validation_ep == 'undefined')
                    form.addClass('validated');

                // Notify others
                form.trigger('pytsite_form_submit', form);

                // Submit form only if it STILL has class 'validated'
                return form.hasClass('validated');
            }

            // Cleaning up error messages
            form.find('.form-messages > div').remove();
            form.find('.form-group').each(function () {
                $(this).removeClass('has-error');
                $(this).find('.help-block.error').remove();
            });

            // Validation form through AJAX call
            form.trigger('pytsite_form_validation');
            pytsite.js.post(validation_ep, form.serializeForm())
                .done(function (data, textStatus, jqXHR) {
                    if (!data.status) {
                        var w_messages = data.messages.widgets;
                        for (widget_uid in w_messages) {
                            var w_group = form.find('.form-group.widget-uid-' + widget_uid).first();
                            w_group.addClass('has-error');
                            for (i in w_messages[widget_uid])
                                w_group.append('<span class="help-block error">' + w_messages[widget_uid][i] + '</span>');
                        }

                        if (data.messages.global.length) {
                            var g_messages = data.messages.global;
                            for (i in g_messages)
                                form.find('.form-messages').append('<div class="alert alert-danger" role="alert">' + g_messages[i] + '</div>')
                        }

                        form.trigger('pytsite_form_validation_fail');

                        $('html, body').animate({
                            scrollTop: $('.has-error').first().offset().top
                        }, 500);
                    }
                    else {
                        form.trigger('pytsite_form_validation_success');
                        form.addClass('validated');
                        form.submit()
                    }

                })
                .fail(function (jqXHR, textStatus, errorThrown) {
                    form.find('.form-messages')
                        .append('<div class="alert alert-danger" role="alert">' + errorThrown + '</div>');

                    form.trigger('pytsite_form_validation_fail');
                });

            return false;
        });
    });
});
