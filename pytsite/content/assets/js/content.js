$(function() {
    var form = $('#odm-ui-form');
    form.find('.widget-uid-title input').blur(function() {
        var titleInput = $(this);
        var descriptionInput = form.find('.widget-uid-description input');

        if(descriptionInput.val() == '')
            descriptionInput.val(titleInput.val());
    });
});