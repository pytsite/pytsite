$(function () {
    $('.widget.geo.location').each(function () {
            var widget = $(this);

            if ('geolocation' in navigator) {
                navigator.geolocation.getCurrentPosition(function (position) {
                    var coords = position.coords;
                    for (k in coords) {
                        var input_selector = null;
                        if (!isNaN(coords[k])) {
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
                                    input_selector = '.alt-accuracy';
                                    break;
                                case 'heading':
                                    input_selector = '.heading';
                                    break;
                                case 'speed':
                                    input_selector = '.speed';
                                    break;
                            }

                            var input = widget.find(input_selector);
                            if (input.length && !input.val())
                                input.val(coords[k]);
                        }
                    }
                });
            }
        }
    );
});
