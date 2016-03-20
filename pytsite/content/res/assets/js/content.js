$(function () {
    var form = $('.odm-ui-form');
    form.find('.widget-uid-description input').focus(function () {
        var descriptionInput = $(this);
        var titleInput = form.find('.widget-uid-title input');

        if (descriptionInput.val() == '')
            descriptionInput.val(titleInput.val());
    });

    // Views count
    $('.content-entity').each(function () {
        var model = $(this).data('model');
        var id = $(this).data('entityId');
        if (model && id) {
            pytsite.ajax.post('pytsite.content.ep.view_count', {
                model: model,
                id: id
            });
        }
    });
});
