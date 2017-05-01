define(['pytsite-lang', 'jquery-color-picker'], function (lang) {
    return function (widget) {
        var input = widget.em.find('input');

        input.css('background-color', '#' + widget.em.data('color'));

        input.colorpicker({
            parts: ['map', 'bar', 'swatches', 'footer'],
            regional: lang.current(),
            colorFormat: '#HEX',
            color: widget.em.data('color'),
            altField: '#' + widget.uid
        });
    }
});
