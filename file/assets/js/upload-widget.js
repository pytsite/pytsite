$(function() {
    $('.widget-files-upload').each(function() {
        var widget = $(this);
        var widgetUid = widget.data('widgetUid');
        //var jfu = widget.find('.jquery-file-upload');
        var addBtn = widget.find('.add-button');
        var postUrl = widget.data('url');
        var maxFiles = parseInt(widget.data('maxFiles'));
        var maxFileSizeMB = parseInt(widget.data('maxFileSize'));
        var maxFileSize = maxFileSizeMB * 1048576;
        var fileInput = widget.find('input[type=file]');

        fileInput.change(function(e) {
            var files = this.files;
            
            for(var i = 0; i < files.length; i++) {
                var file = files[i];
                var formData = new FormData();

                if(maxFileSize && file.size > maxFileSize) {
                    alert(t('pytsite.file@file_too_big', {
                        file_name: file.name,
                        max_size: maxFileSizeMB
                    }));

                    continue;
                }

                formData.append(widgetUid, file);

                $.ajax({
                    type: 'POST',
                    url: postUrl,
                    data: formData,
                    processData: false,
                    contentType: false
                });
            }


        });
    });
});