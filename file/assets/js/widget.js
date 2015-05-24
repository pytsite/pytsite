Dropzone.autoDiscover = false;

$(function() {
    $('.widget-files-upload').each(function() {
        var widget = $(this);
        var widgetUid = widget.data('widgetUid');
        var dzCont = $(this).find('.dropzone').first();

        dzCont.dropzone({
            url: '/pytsite/file/upload/' + widget.data('model'),
            uploadMultiple: false,
            paramName: widgetUid,
            addRemoveLinks: true
        });

        dz = dzCont[0].dropzone;

        dz.on('success', function(file, response) {
            console.log(file);
            console.log(response);
            for(i in response) {
                widget.append('<input type="hidden" name="'+widgetUid+'[]" value="'+response[i]+'">');
            }
        });

        dz.on('removedfile', function(file) {
            console.log(file);
        });

    });
});