$.fn.extend({
    widgetFilesUpload: function () {
        var widget = this;
        if (!widget.length)
            return;

        var slots = widget.find('.slots');
        var widgetUid = widget.data('uid');
        var addBtn = widget.find('.add-button');
        var postUrl = widget.data('url');
        var maxFiles = parseInt(widget.data('maxFiles'));
        var maxFileSizeMB = parseInt(widget.data('maxFileSize'));
        var maxFileSize = maxFileSizeMB * 1048576;
        var fileInput = widget.find('input[type=file]');
        var filesCount = 0;
        var acceptedFileTypes = fileInput.prop('accept');
        var progressSlot = widget.find('.progress');
        var progressBar = progressSlot.find('.progress-bar');
        var slotCss = widget.data('slotCss');

        if (acceptedFileTypes != '*/*')
            acceptedFileTypes = acceptedFileTypes.split('/')[0];

        var sortableInit = function () {
            if (slots.hasClass('ui-sortable')) {
                slots.sortable('refresh');
            }
            else {
                slots.sortable({
                    containment: 'parent',
                    cursor: 'move',
                    revert: true,
                    tolerance: 'pointer',
                    items: '> .slot.sortable',
                    forcePlaceholderSize: true,
                    placeholder: 'slot placeholder ' + slotCss,
                    update: renumberSlots
                });
            }
        };

        var setupSlot = function (slot) {
            // 'Remove' button click event handler
            $(slot).find('.btn-remove').click(function () {
                removeSlot(slot)
            });

            return $(slot);
        };

        var createSlot = function (fid, thumb_url) {
            var slot = $('<div class="slot sortable ' + slotCss + '" data-fid="' + fid + '">');
            var inner = $('<div class="inner">');

            slot.append(inner);
            inner.append($('<div class="thumb"><img class="img-responsive" src="{u}"></div>'.replace('{u}', thumb_url)));
            inner.append($('<button type="button" class="btn btn-danger btn-xs btn-remove"><i class="fa fa-remove"></i></button>'));
            inner.append($('<span class="number">'));
            inner.append('<input type="hidden" name="' + widgetUid + '[]" value="' + fid + '">');

            return setupSlot(slot);
        };

        var renumberSlots = function () {
            var n = 1;
            filesCount = 0;
            widget.find('.slot .number').each(function () {
                $(this).text(n++);
                ++filesCount;
            });

            if (filesCount >= maxFiles) {
                addBtn.hide();
                widget.addClass('max-files-reached');
            }
            else {
                addBtn.show();
                widget.removeClass('max-files-reached');
            }
        };

        var appendSlot = function (slot) {
            slots.append(slot);
            progressSlot.insertAfter(slots.find('.slot:last-child'));
            addBtn.insertAfter(slots.find('.slot:last-child'));
            renumberSlots();
            sortableInit();
        };

        var removeSlot = function (slot) {
            var fid = $(slot).data('fid');
            if (confirm(t('pytsite.file@really_delete'))) {
                widget.find('input[value="' + fid + '"]').remove();
                widget.append('<input type="hidden" name="' + widgetUid + '_to_delete" value="' + fid + '">');
                $(slot.remove());
                renumberSlots();

                --filesCount;
                addBtn.show();
                widget.removeClass('max-files-reached');

                sortableInit();
            }
        };

        var uploadFile = function (file) {
            if (acceptedFileTypes != '*/*' && file.type.split('/')[0] != acceptedFileTypes) {
                alert(t('pytsite.file@file_has_invalid_type'));
                return false;
            }

            if (maxFileSize && file.size > maxFileSize) {
                alert(t('pytsite.file@file_too_big', {
                    file_name: file.name,
                    max_size: maxFileSizeMB
                }));

                return false;
            }

            var formData = new FormData();
            formData.append(widgetUid, file);

            ++filesCount;

            if (filesCount == maxFiles)
                widget.addClass('max-files-reached');

            if (filesCount > maxFiles) {
                filesCount = maxFiles;
                progressSlot.hide();
                alert(t('pytsite.file@max_files_exceeded'));

                return false;
            }

            $.ajax({
                type: 'POST',
                url: postUrl,
                data: formData,
                processData: false,
                contentType: false,
                beforeSend: function () {
                    progressBar.css('width', '0');
                    progressBar.attr('aria-valuenow', '0');
                    progressBar.text('0%');
                    progressSlot.show();
                    addBtn.hide();
                },
                xhr: function () {  // Custom XMLHttpRequest
                    var myXhr = $.ajaxSettings.xhr();
                    if (myXhr.upload) { // Check if upload property exists
                        myXhr.upload.addEventListener('progress', function (evt) {
                            var percentage = parseInt(evt.loaded / evt.total * 100);
                            progressBar.css('width', percentage + '%');
                            progressBar.attr('aria-valuenow', percentage);
                            progressBar.text(percentage + '%');
                        });
                    }
                    return myXhr;
                }
            }).success(function (data, textStatus, jqXHR) {
                $.each(data, function (k, v) {
                    progressSlot.hide();
                    appendSlot(createSlot(v['fid'], v['thumb_url']));
                })
            }).fail(function (jqXHR, textStatus, errorThrown) {
                --filesCount;
                progressSlot.hide();
                addBtn.show();
                widget.removeClass('max-files-reached');
                alert(errorThrown);
            });
        };

        fileInput.change(function (e) {
            var files = this.files;

            for (var i = 0; i < files.length; i++) {
                var file = files[i];

                // Image resizing
                var maxWidth = parseInt(widget.data('imageMaxWidth'));
                var maxHeight = parseInt(widget.data('imageMaxHeight'));
                if (file.type.split('/')[0] == 'image' && (maxWidth || maxHeight)) {
                    // Resizing image
                    loadImage(file, function (canvas) {
                        canvas.toBlob(function (resizedImage) {
                            resizedImage.name = file.name;
                            // Attaching metadata
                            loadImage.parseMetaData(file, function (metaData) {
                                if (metaData.imageHead) {
                                    resizedImage = new Blob([
                                        metaData.imageHead,
                                        loadImage.blobSlice.call(resizedImage, 20)
                                    ], {type: resizedImage.type, name: resizedImage.name});
                                }
                                uploadFile(resizedImage);
                            });
                        }, file.type);
                    }, {
                        canvas: true,
                        maxWidth: maxWidth,
                        maxHeight: maxHeight
                    });
                }
                else
                    uploadFile(file);
            }
        });

        // Initial setup of existing slots
        progressSlot.removeClass('hidden').hide();
        widget.find('.slot').each(function () {
            setupSlot(this);
        });
        renumberSlots();
        sortableInit();
    }
});

$(window).on('pytsite.widget.init:pytsite.file._widget.FilesUpload', function (e, widget) {
    widget.widgetFilesUpload();
});
