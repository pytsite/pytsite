define(['jquery', 'assetman', 'twitter-bootstrap-tokenfield'], function ($, assetman) {
    assetman.loadCSS('pytsite.widget@css/tokens.css');

    return function (widget) {
        var widgetInput = widget.em.find('input');
        var localSource = widget.em.data('localSource');
        var remoteSource = widget.em.data('remoteSource');
        var tokenFieldOptions = {
            beautify: false,
            autocomplete: {
                minLength: 2,
                delay: 250
            }
        };

        // TODO: local source support.

        if (remoteSource) {
            tokenFieldOptions.autocomplete.source = function (request, response) {
                var term = request['term'].trim();
                if (!term.length)
                    return;

                var url = remoteSource.replace('__QUERY', term);
                var req_data = {
                    'exclude': widgetInput.val().split(',')
                };

                $.getJSON(url, req_data, function (resp_data) {
                    response(resp_data);
                });
            }
        }

        widgetInput.tokenfield(tokenFieldOptions);

        var widgetTokenInput = widget.em.find('#' + widgetInput.attr('id') + '-tokenfield');

        widgetInput.on('tokenfield:createtoken', function (e) {
            e.attrs.label = e.attrs.label.trim();
            e.attrs.value = e.attrs.value.trim();

            var existingTerms = widgetInput.val().split(',');
            var newTerm = e.attrs.value.trim();

            if (existingTerms.indexOf(newTerm) >= 0) {
                widgetTokenInput.val('');
                return false;
            }
        });

        widgetInput.on('tokenfield:createdtoken', function () {
            widgetTokenInput.autocomplete('close');
        });
    }
});
