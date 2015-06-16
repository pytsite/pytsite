$(function () {
    $('.widget-typeahead-text-input').each(function () {
        var widget = $(this);
        var input = widget.find('input');
        var url = widget.data('sourceUrl');

        var engine = new Bloodhound({
            datumTokenizer: Bloodhound.tokenizers.obj.whitespace,
            queryTokenizer: Bloodhound.tokenizers.whitespace,
            remote: {
                url: url,
                wildcard: '__QUERY'
            }
        });

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
            source: engine
        });
    });
});