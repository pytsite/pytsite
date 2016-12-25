$(window).on('pytsite.widget.init:pytsite.widget._select.ColorPicker', function (e, widget) {
    var input = widget.em.find('input');

    input.css('background-color', '#' + widget.em.data('color'));

    input.colorpicker({
        parts: ['map', 'bar', 'swatches', 'footer'],
        regional: pytsite.lang.current(),
        colorFormat: '#HEX',
        color: widget.em.data('color'),
        altField: '#' + widget.uid
    });
});
