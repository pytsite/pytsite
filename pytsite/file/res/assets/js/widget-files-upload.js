define(['jquery', 'assetman', 'pytsite-http-api', 'pytsite-lang', 'load-image', 'jquery-ui'], function ($, assetman, httpApi, lang, loadImage) {
    return function (widget) {
        var widgetEm = widget.em;
        var slotsEm = widgetEm.find('.slots');
        var widgetUid = widgetEm.data('uid');
        var model = widgetEm.data('model');
        var addBtn = widgetEm.find('.add-button');
        var postUrl = widgetEm.data('url');
        var maxFiles = parseInt(widgetEm.data('maxFiles'));
        var maxFileSizeMB = parseInt(widgetEm.data('maxFileSize'));
        var maxFileSize = maxFileSizeMB * 1048576;
        var fileInput = widgetEm.find('input[type=file]');
        var filesCount = 0;
        var acceptedFileTypes = fileInput.prop('accept');
        var progressSlot = widgetEm.find('.progress');
        var progressBar = progressSlot.find('.progress-bar');
        var slotCss = widgetEm.data('slotCss');
        var showNumbers = widgetEm.data('showNumbers') === 'True';
        var dnd = widgetEm.data('dnd') === 'True';

        if (acceptedFileTypes !== '*/*')
            acceptedFileTypes = acceptedFileTypes.split('/')[0];

        assetman.loadCSS('pytsite.file@css/widget-files-upload.css');

        function sortableSetup() {
            if (!dnd)
                return;

            if (slotsEm.hasClass('ui-sortable')) {
                slotsEm.sortable('refresh');
            }
            else {
                slotsEm.sortable({
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
        }

        function setupSlot(slot) {
            // 'Remove' button click event handler
            $(slot).find('.btn-remove').click(function () {
                removeSlot(slot)
            });

            return $(slot);
        }

        function createSlot(uid, thumb_url) {
            var slot = $('<div class="slot content sortable ' + slotCss + '" data-uid="' + uid + '">');
            var inner = $('<div class="inner">');

            slot.append(inner);
            inner.append($('<div class="thumb"><img class="img-responsive" src="{u}"></div>'.replace('{u}', thumb_url)));
            inner.append($('<button type="button" class="btn btn-danger btn-xs btn-remove"><i class="fa fa-remove"></i></button>'));
            if (showNumbers)
                inner.append($('<span class="number">'));
            inner.append('<input type="hidden" name="' + widgetUid + '[]" value="' + uid + '">');

            return setupSlot(slot);
        }

        function renumberSlots() {
            var n = 1;
            filesCount = 0;
            widgetEm.find('.slot.content').each(function () {
                if (showNumbers)
                    $(this).find('.number').text(n++);

                ++filesCount;
            });

            if (filesCount >= maxFiles) {
                addBtn.hide();
                widgetEm.addClass('max-files-reached');
            }
            else {
                addBtn.show();
                widgetEm.removeClass('max-files-reached');
            }
        }

        function appendSlot(slot) {
            slotsEm.append(slot);
            progressSlot.insertAfter(slotsEm.find('.slot:last-child'));
            addBtn.insertAfter(slotsEm.find('.slot:last-child'));

            renumberSlots();
            sortableSetup();
        }

        function removeSlot(slot, confirmDelete) {
            var uid = $(slot).data('uid');

            if (confirmDelete !== false && !confirm(lang.t('pytsite.file@really_delete')))
                return;

            widgetEm.find('input[value="' + uid + '"]').remove();
            widgetEm.append('<input type="hidden" name="' + widgetUid + '_to_delete" value="' + uid + '">');
            $(slot.remove());
            renumberSlots();

            --filesCount;
            addBtn.show();
            widgetEm.removeClass('max-files-reached');

            sortableSetup();
        }

        function uploadFile(file) {
            if (acceptedFileTypes !== '*/*' && file.type.split('/')[0] !== acceptedFileTypes) {
                alert(lang.t('pytsite.file@file_has_invalid_type'));
                return false;
            }

            if (maxFileSize && file.size > maxFileSize) {
                alert(lang.t('pytsite.file@file_too_big', {
                    file_name: file.name,
                    max_size: maxFileSizeMB
                }));

                return false;
            }

            var formData = new FormData();
            formData.append(widgetUid, file);

            ++filesCount;

            if (filesCount === maxFiles)
                widgetEm.addClass('max-files-reached');

            if (filesCount > maxFiles) {
                filesCount = maxFiles;
                progressSlot.hide();
                alert(lang.t('pytsite.file@max_files_exceeded'));

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

                    $(widget).trigger('fileUploadStart');
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
            }).success(function (data) {
                $.each(data, function (k, v) {
                    httpApi.get('file' + '/' + v['uid']).done(function (r) {
                        progressSlot.hide();
                        appendSlot(createSlot(r['uid'], r['thumb_url']));
                        $(widget).trigger('fileUploadSuccess', [v]);
                    });
                });
            }).fail(function (jqXHR, textStatus, errorThrown) {
                --filesCount;
                progressSlot.hide();
                addBtn.show();
                widgetEm.removeClass('max-files-reached');
                $(widget).trigger('fileUploadFail');
                alert(errorThrown);
            });
        }

        fileInput.change(function () {
            var files = this.files;

            $(widget).trigger('widgetChange');

            for (var i = 0; i < files.length; i++) {
                var file = files[i];

                // Image resizing
                var maxWidth = parseInt(widgetEm.data('imageMaxWidth'));
                var maxHeight = parseInt(widgetEm.data('imageMaxHeight'));
                if (file.type.split('/')[0] === 'image' && (maxWidth || maxHeight)) {
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

                                // Upload resized image
                                uploadFile(resizedImage);
                            });
                        }, file.type);
                    }, {
                        canvas: true,
                        maxWidth: maxWidth,
                        maxHeight: maxHeight
                    });
                }
                else {
                    uploadFile(file);
                }
            }
        });

        // Open file select dialog
        widget.open = function () {
            $(widget).trigger('widgetOpen');
            fileInput[0].click();
        };

        // Remove all existing slots
        widget.clear = function (confirmDelete) {
            fileInput.val('');

            slotsEm.find('.slot.content').each(function () {
                removeSlot(this, confirmDelete);
            });

            $(widget).trigger('widgetClear');
        };

        // Initial setup of existing slots
        progressSlot.removeClass('hidden').hide();
        widgetEm.find('.slot').each(function () {
            setupSlot(this);
        });

        renumberSlots();
        sortableSetup();
    }
});
