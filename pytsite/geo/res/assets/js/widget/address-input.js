$(function () {
    function setBounds(autcomplete) {
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(function (position) {
                var geolocation = new google.maps.LatLng(position.coords.latitude, position.coords.longitude);
                var circle = new google.maps.Circle({center: geolocation, radius: position.coords.accuracy});

                autcomplete.setBounds(circle.getBounds());
            });
        }
    }

    $('.widget.geo.search-address').each(function () {
        var widget = $(this);
        var uid = widget.data('widget-uid');
        var searchInput = widget.find('input[name="' + uid + '[search]"]');
        var addressInput = widget.find('input[name="' + uid + '[address]"]');
        var lngLatInput = widget.find('input[name="' + uid + '[lng_lat]"]');
        var componentsInput = widget.find('input[name="' + uid + '[components]"]');
        var autocomplete = new google.maps.places.Autocomplete(searchInput[0], {
            types: ['geocode']
        });

        widget.keydown(function (event) {
            if (event.keyCode == 13) {
                event.preventDefault();
                return false;
            }
        });

        searchInput.focus(function () {
            this.select()
        });

        searchInput.blur(function () {
            if (!$(this).val().length) {
                addressInput.val('');
                lngLatInput.val('').trigger('change');
                componentsInput.val('');
            }

            setTimeout(function () {
                if (addressInput.val())
                    searchInput.val(addressInput.val());
                else
                    searchInput.val('');
            }, 50);
        });

        google.maps.event.addListener(autocomplete, 'place_changed', function () {
            var place = autocomplete.getPlace();
            if (place.hasOwnProperty('geometry')) {
                var loc = place.geometry.location;
                addressInput.val(searchInput.val());
                lngLatInput.val(JSON.stringify([loc.lng(), loc.lat()])).trigger('change');
                componentsInput.val(JSON.stringify(place.address_components));
            }
        });

        // Automatic location detection
        var autodetect = parseInt(widget.data('autodetect'));
        if (autodetect) {
            setBounds(autocomplete);

            if (autodetect && !searchInput.val() && navigator.geolocation) {
                navigator.geolocation.getCurrentPosition(function (position) {
                    var geoCoder = new google.maps.Geocoder();
                    var latLng = new google.maps.LatLng(position.coords.latitude, position.coords.longitude);
                    geoCoder.geocode({'latLng': latLng}, function (results, status) {
                        if (status == google.maps.GeocoderStatus.OK && results.length) {
                            var place = results[0];
                            var loc = place.geometry.location;
                            searchInput.val(place.formatted_address);
                            addressInput.val(place.formatted_address);
                            lngLatInput.val(JSON.stringify([loc.lng(), loc.lat()])).trigger('change');
                            componentsInput.val(JSON.stringify(place.address_components));
                        }
                    });
                });
            }
        }
    });
});