$(function() {
    $('.widget-token-input').each(function() {
        var widget = $(this);
        var widgetInput = widget.find('input');
        var localSource = widget.data('localSource');
        var remoteSource = widget.data('remoteSource');
        var engineConfig = {
            datumTokenizer: Bloodhound.tokenizers.whitespace,
            queryTokenizer: Bloodhound.tokenizers.whitespace
        };

        if(localSource != undefined)
            engineConfig.local = localSource.split(',');

        if(remoteSource != undefined) {
            engineConfig.remote = {
                url: remoteSource,
                prepare: function(query, settings) {
                    settings.url = settings.url.replace('__QUERY', query);
                    settings.data = {
                        'exclude': widgetInput.val().split(',')
                    };
                    return settings;
                }
            };
        }

        var engine = new Bloodhound(engineConfig);

        engine.initialize();
        widgetInput.tokenfield({
            beautify: false,
            typeahead: [{hint: false, highlight: true}, {source: engine}]
        });
    });
});