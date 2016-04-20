$(window).on('pytsite.widget.init:pytsite.widget._select.TrafficLightScore', function (e, widget) {
    $(window).trigger('pytsite.widget.init:pytsite.widget._select.Score', [widget]);
});
