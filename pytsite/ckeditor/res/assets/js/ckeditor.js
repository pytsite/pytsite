$(window).on('pytsite.widget.init:pytsite.ckeditor._widget.CKEditor', function (e, widget) {
    widget.em.find('textarea').each(function () {
        var editor = $(this).ckeditor({
            title: false,
            extraPlugins: 'youtube,codesnippet,stylescombo',
            language: pytsite.lang.current(),
            filebrowserUploadUrl: pytsite.httpApi.url('file/upload'),
            height: 500,
            toolbar: [
                ['Bold', 'Italic', '-', 'Underline', 'Strike', '-', 'Subscript', 'Superscript', '-', 'Format', 'RemoveFormat'],
                ['NumberedList', 'BulletedList', '-', 'Outdent', 'Indent', '-', 'Blockquote', '-', 'JustifyLeft', 'JustifyCenter', 'JustifyRight'],
                ['Link', 'Unlink'],
                ['PasteText', 'PasteFromWord', '-', 'Undo', 'Redo'],
                ['Image', 'Youtube', 'CodeSnippet', 'Iframe', 'Table', 'HorizontalRule', 'SpecialChar', 'Styles'],
                ['ShowBlocks', 'Source', 'Maximize']
            ],
            coreStyles_italic: {
                element: 'i'
            },
            extraAllowedContent: 'div p blockquote img ul ol li a i span[data-*,hidden,lang](*);script[*];code(*);pre(*)',
            disableNativeSpellChecker: false
        }).editor;

        editor.on('change', function() {
            this.updateElement();
        });
    });
});
