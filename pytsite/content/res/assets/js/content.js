$(function () {
    var form = $('#odm-ui-form');
    form.find('.widget-uid-title input').blur(function () {
        var titleInput = $(this);
        var descriptionInput = form.find('.widget-uid-description input');

        if (descriptionInput.val() == '')
            descriptionInput.val(titleInput.val());
    });

    // Views count
    $('.content-entity').each(function () {
        var model = $(this).data('model');
        var id = $(this).data('entityId');
        if (model && id) {
            pytsite.js.post('pytsite.content.eps.view_count', {
                model: model,
                id: id
            });
        }
    });
});
