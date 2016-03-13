$(function () {
    $('.widget-typeahead-text-input').each(function () {
        var widget = $(this);
        var input = widget.find('input');

        widget.keydown(function (event) {
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
                    url: widget.data('sourceUrl'),
                    wildcard: '__QUERY'
                }
            })
        });
    });
});