$(window).on('pytsite.widget.init:pytsite.geo._widget.Location', function (e, widget) {
    if (widget.em.data('autodetect') != 'True')
        return;

    if (!('geolocation' in navigator))
        throw 'Your browser does not support geo location.';

    navigator.geolocation.watchPosition(function (position) {
        var coords = position.coords;

        for (var k in coords) {
            var input_selector = null;
            if (k in coords && !isNaN(coords[k])) {
                switch (k) {
                    case 'latitude':
                        input_selector = '.lat';
                        break;
                    case 'longitude':
                        input_selector = '.lng';
                        break;
                    case 'altitude':
                        input_selector = '.alt';
                        break;
                    case 'accuracy':
                        input_selector = '.accuracy';
                        break;
                    case 'altitudeAccuracy':
                        input_selector = '.alt_accuracy';
                        break;
                    case 'heading':
                        input_selector = '.heading';
                        break;
                    case 'speed':
                        input_selector = '.speed';
                        break;
                }

                var input = widget.em.find(input_selector);
                if (input.length) {
                    input.val(coords[k]);
                    input.change();
                }
            }
        }

        widget.em.find('.text').text('Longitude: ' + coords.longitude + ', latitude: ' + coords.latitude);
    }, function (err) {
        console.error(err);
    }, {
        enableHighAccuracy: true
    });
});
