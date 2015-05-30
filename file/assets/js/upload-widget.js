$.fn.extend({
    widgetFilesUpload: function() {
        var widget = this;
        var widgetUid = widget.data('widgetUid');
        var addBtn = widget.find('.add-button');
        var processIcon = widget.find('.processing');
        var postUrl = widget.data('url');
        var maxFiles = parseInt(widget.data('maxFiles'));
        var maxFileSizeMB = parseInt(widget.data('maxFileSize'));
        var maxFileSize = maxFileSizeMB * 1048576;
        var fileInput = widget.find('input[type=file]');
        var filesCount = 0;
        var acceptedFileTypes = fileInput.prop('accept');

        if(acceptedFileTypes != '*/*')
            acceptedFileTypes = acceptedFileTypes.split('/')[0];

        var setupSlot = function(slot) {
            $(slot).find('.btn-remove').click(function() {
                removeSlot(slot)
            });

            return $(slot);
        };

        var createSlot = function(fid, thumb_url) {
            var slot = $('<div class="slot" data-fid="'+fid+'">');
            slot.append($('<div class="thumb"><img src="{u}"></div>'.replace('{u}', thumb_url)));
            slot.append($('<button type="button" class="btn btn-danger btn-sm btn-remove"><i class="fa fa-remove"></i></button>'));
            slot.append($('<span class="number">'));
            widget.append('<input type="hidden" name="'+widgetUid+'" value="'+fid+'">');
            return setupSlot(slot);
        };

        var renumberSlots = function () {
            var n = 1;
            filesCount = 0;
            widget.find('.slot .number').each(function() {
                $(this).text(n++);
                ++filesCount;
            });

            if(filesCount >= maxFiles) {
                addBtn.hide();
                widget.addClass('max-files-reached');
            }
        };

        var appendSlot = function(slot) {
            widget.find('.slots').append(slot);
            renumberSlots();
        };

        var removeSlot = function(slot) {
            var fid = $(slot).data('fid');
            if(confirm(t('pytsite.file@really_delete'))) {
                widget.find('input[value="'+fid+'"]').remove();
                widget.append('<input type="hidden" name="'+widgetUid+'_to_delete" value="'+fid+'">');
                $(slot.remove());
                renumberSlots();

                --filesCount;
                addBtn.show();
                widget.removeClass('max-files-reached');
            }
        };

        fileInput.change(function(e) {
            var files = this.files;

            processIcon.show();

            for(var i = 0; i < files.length; i++) {
                var file = files[i];
                var formData = new FormData();

                if(acceptedFileTypes != '*/*' && file.type.split('/')[0] != acceptedFileTypes) {
                    alert(t('pytsite.file@file_has_invalid_type'));
                    continue;
                }

                if(maxFileSize && file.size > maxFileSize) {
                    alert(t('pytsite.file@file_too_big', {
                        file_name: file.name,
                        max_size: maxFileSizeMB
                    }));
                    continue;
                }

                ++filesCount;

                if(filesCount == maxFiles) {
                    addBtn.hide();
                    widget.addClass('max-files-reached');
                }

                if(filesCount > maxFiles) {
                    --filesCount;
                    processIcon.hide();
                    alert(t('pytsite.file@max_files_exceeded'));
                    return false;
                }

                formData.append(widgetUid, file);

                $.ajax({
                    type: 'POST',
                    url: postUrl,
                    data: formData,
                    processData: false,
                    contentType: false
                }).success(function(data, textStatus, jqXHR) {
                    $.each(data, function(k, v) {
                        appendSlot(createSlot(v['fid'], v['thumb_url']));
                    })
                }).fail(function(jqXHR, textStatus, errorThrown ) {
                    --filesCount;
                    addBtn.show();
                    widget.removeClass('max-files-reached');
                    processIcon.hide();
                    alert(errorThrown);
                });
            }

            processIcon.hide();
        });

        // Initial setup of existing slots
        processIcon.hide();
        widget.find('.slot').each(function() {
            setupSlot(this);
        });
        renumberSlots();
    }
});



$(function() {
    $('.widget-files-upload').widgetFilesUpload();
});