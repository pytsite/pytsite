define(['assetman', 'pytsite-http-api'], function (assetman, httpApi) {
    assetman.loadCSS('pytsite.widget@css/file.css');

    function appendSlot(cont, num, name, msg) {
        var slot = $('<div class="slot num-' + num + '"></div>');

        slot.append('<span class="name">' + name + '</span>');
        slot.append('<span class="msg">' + msg + '</span>');
        cont.append(slot);
    }

    function updateSlot(cont, num, msg, css) {
        var slot = cont.find('.slot.num-' + num);
        slot.find('.msg').text(msg);

        if (css !== undefined) {
            slot.addClass(css);
        }
    }

    return function (widget) {
        var endpoint = widget.data('uploadEndpoint');
        if (!endpoint)
            return;

        var inp = widget.em.find('input').first();
        var slots = $('<div class="slots"></div>');
        var maxFilesCount = parseInt(widget.data('maxFiles'));
        var addedFilesCount = 0;
        var uploadingFilesCount = 0;
        var uploadedFilesCount = 0;

        inp.before(slots);

        widget.em.change(function () {
            for (var i = 0; i < inp[0].files.length; i++) {
                if (uploadingFilesCount + uploadedFilesCount >= maxFilesCount)
                    continue;

                var data = new FormData();
                var file = inp[0].files[i];
                data.append('index', addedFilesCount);
                data.append(inp[0].name, file);
                inp.attr('disabled', true);

                appendSlot(slots, addedFilesCount, file.name, 'Uploading...');
                ++addedFilesCount;
                ++uploadingFilesCount;

                httpApi.post(endpoint, data).done(function (r) {
                    if ('message' in r)
                        updateSlot(slots, r.index, r.message);

                    if ('eval' in r)
                        eval(r.eval);

                    ++uploadedFilesCount;
                }).fail(function (r) {
                    if ('index' in r.responseJSON) {
                        updateSlot(slots, r.responseJSON.index, r.responseJSON.error, 'has-error');
                    }
                    else {
                        widget.setState('error');
                        widget.addMessage(r.responseJSON.error)
                    }
                }).always(function () {
                    inp.attr('disabled', false);
                    --uploadingFilesCount;

                    if (uploadedFilesCount === maxFilesCount)
                        inp.hide();
                });
            }

            var newInp = $('<input type="file" name="' + inp.attr('name') + '">');
            inp.replaceWith(newInp);
            inp = newInp;
        });
    };
});
