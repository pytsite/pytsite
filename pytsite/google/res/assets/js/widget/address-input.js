$(function () {
    function setBounds(autcomplete) {
        if ('geolocation' in navigator) {
            navigator.geolocation.getCurrentPosition(function (position) {
                var geolocation = new google.maps.LatLng(position.coords.latitude, position.coords.longitude);
                var circle = new google.maps.Circle({center: geolocation, radius: position.coords.accuracy});

                autcomplete.setBounds(circle.getBounds());
            });
        }
    }

    $('.widget-google-address-input').each(function () {
        var widget = $(this);
        var uid = widget.data('widget-uid');
        var searchInput = widget.find('input[name="' + uid + '[search]"]');
        var addressInput = widget.find('input[name="' + uid + '[address]"]');
        var lngInput = widget.find('input[name="' + uid + '[lng]"]');
        var latInput = widget.find('input[name="' + uid + '[lat]"]');
        var componentsInput = widget.find('input[name="' + uid + '[address_components]"]');
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
                latInput.val('0.0');
                lngInput.val('0.0');
                componentsInput.val('[]');
            }

            setTimeout(function () {
                if (addressInput.val())
                    searchInput.val(addressInput.val());
                else
                    searchInput.val('');
            }, 50);
        });

        // Update our hidden fields with data provided by Google
        google.maps.event.addListener(autocomplete, 'place_changed', function () {
            var place = autocomplete.getPlace();
            if (place.hasOwnProperty('geometry')) {
                var loc = place.geometry.location;
                addressInput.val(searchInput.val());
                latInput.val(loc.lat());
                lngInput.val(loc.lng());
                componentsInput.val(JSON.stringify(place.address_components));
            }
        });

        // Automatic location detection
        if (widget.data('autodetect') == 'True' && !addressInput.val() && 'geolocation' in navigator) {
            setBounds(autocomplete);
            navigator.geolocation.getCurrentPosition(function (position) {
                var geoCoder = new google.maps.Geocoder();
                var latLng = new google.maps.LatLng(position.coords.latitude, position.coords.longitude);
                geoCoder.geocode({'latLng': latLng}, function (results, status) {
                    if (status == google.maps.GeocoderStatus.OK && results.length) {
                        var place = results[0];
                        var loc = place.geometry.location;

                        searchInput.val(place.formatted_address);
                        addressInput.val(place.formatted_address);
                        lngInput.val(loc.lng());
                        latInput.val(loc.lat());
                        componentsInput.val(JSON.stringify(place.address_components));
                    }
                });
            });
        }
    });
});