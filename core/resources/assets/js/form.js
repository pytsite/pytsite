$.fn.serializeForm = function() {
    var o = {};
    var a = this.serializeArray();
    $.each(a, function() {
        if (o[this.name] !== undefined) {
            if (!o[this.name].push) {
                o[this.name] = [o[this.name]];
            }
            o[this.name].push(this.value || '');
        } else {
            o[this.name] = this.value || '';
        }
    });
    return o;
};

$(function() {
    $('.pytsite-form').each(function() {
        var form = $(this);

        form.submit(function(e) {
            var validation_ep = form.data('validationEp');

            // Cleaning up error messages
            form.find('.form-group').each(function() {
                $(this).removeClass('has-error');
                $(this).find('.help-block.error').remove();
            });

            // No validation is defined, submitting form
            if(typeof validation_ep == 'undefined')
                return true;

            var response = pytsite.js_api.post(validation_ep, form.serializeForm());

            if(!response.status) {
                for(widget_uid in response.messages) {
                    var w_group = form.find('.form-group.widget-uid-'+widget_uid).first();
                    w_group.addClass('has-error');
                    for(i in response.messages[widget_uid])
                        w_group.append('<span class="help-block error">' + response.messages[widget_uid][i] + '</span>');
                }
            }

            return false;
        });
    });
});