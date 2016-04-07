$(window).on('pytsite.widget.init:pytsite.geo._widget.Location', function (e, widget) {
    // Change widget's value only if it's not empty
    if (widget.em.find('.text').val().replace(' ', '') != '')
        return;

    if (!('geolocation' in navigator))
        throw 'Your browser does not provide geo location.';

    navigator.geolocation.getCurrentPosition(function (position) {
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
                if (input.length && input.val() == '0.0') {
                    input.val(coords[k]);
                    input.change();
                }
            }
        }

        // Helper field which used on backend to build indexes
        widget.em.find('.lng_lat').val(JSON.stringify([coords.longitude, coords.latitude])).change();

        widget.em.find('.text').text('Longitude: ' + coords.longitude + ', latitude: ' + coords.latitude);
    });
});
