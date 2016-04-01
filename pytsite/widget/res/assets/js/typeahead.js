$(window).on('pytsite.widget.init', function (e, widget) {
    widget.em.find('.widget-typeahead-text-input').each(function () {
        var input = $(this).find('input');

        $(this).keydown(function (event) {
            if (event.keyCode == 13) {
                event.preventDefault();
                input.typeahead('close');
            }
        });

        input.typeahead({
            highlight: true,
            hint: true
        }, {
            source: new Bloodhound({
                datumTokenizer: Bloodhound.tokenizers.mapObject.whitespace,
                queryTokenizer: Bloodhound.tokenizers.whitespace,
                remote: {
                    url: $(this).data('sourceUrl'),
                    wildcard: '__QUERY'
                }
            })
        });
    });
});
