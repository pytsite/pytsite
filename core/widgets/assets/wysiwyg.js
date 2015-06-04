$(function() {
    $('.widget-wysiwyg').each(function() {
        var widget = $(this);
        widget.find('textarea').ckeditor();
    });
});