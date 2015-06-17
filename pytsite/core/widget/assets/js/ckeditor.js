$(function() {
    $('.widget-ckeditor').each(function() {
        var widget = $(this);
        widget.find('textarea').ckeditor({
            extraPlugins: 'youtube',
            language: pytsite.lang.current_lang,
            filebrowserUploadUrl: '/not/implemented',
            height: 500,
            toolbar: [
                ['Bold','Italic','-','Underline','Strike','-','Subscript','Superscript','-','Format','RemoveFormat'],
                ['NumberedList','BulletedList','-','Outdent','Indent','-','Blockquote','-','JustifyLeft','JustifyCenter','JustifyRight'],
                ['Link', 'Unlink'],
                ['PasteText','PasteFromWord','-','Undo','Redo'],
                ['Image','Youtube','Iframe','Table', 'HorizontalRule','SpecialChar'],
                ['ShowBlocks','Source','Maximize']
            ],
            coreStyles_italic: {
                element : 'i'
            },
            extraAllowedContent: 'div p span(*);a[data-*](*);i(*);'
        });
    });
});