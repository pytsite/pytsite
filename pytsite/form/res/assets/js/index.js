require(['jquery', 'pytsite-form', 'assetman'], function ($, form, assetman) {
    $('.pytsite-form').each(function () {
        // Create form
        var frm = new form.Form($(this));

        // If requested to walk to particular step automatically
        var q = assetman.parseLocation().query;
        var walkToStep = '__form_data_step' in q ? parseInt(q['__form_data_step']) : 1;
        $(frm.em).on('formForward', function () {
            // When form will make its first step, move it automatically to the requested step
            if (frm.currentStep < walkToStep)
                frm.forward();
        });

        // Do the first step
        frm.forward();
    });
});
