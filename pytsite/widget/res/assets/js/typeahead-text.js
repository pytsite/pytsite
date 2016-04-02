$(window).on('pytsite.widget.init:pytsite.widget._input.TypeaheadText', function (e, widget) {
    $(widget).keydown(function (event) {
        if (event.keyCode == 13) {
            event.preventDefault();
            input.typeahead('close');
        }
    });

    $(widget).find('input').typeahead({
        highlight: true,
        hint: true
    }, {
        source: new Bloodhound({
            datumTokenizer: Bloodhound.tokenizers.mapObject.whitespace,
            queryTokenizer: Bloodhound.tokenizers.whitespace,
            remote: {
                url: $(widget).data('sourceUrl'),
                wildcard: '__QUERY'
            }
        })
    });
});
