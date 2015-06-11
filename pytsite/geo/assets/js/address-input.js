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

    $('.widget-geo-address-input').each(function () {
        var widget = $(this);
        var searchInput = widget.find('input[type=text]').first();
        var addressInput = $('<input type="hidden" name="' + widget.data('widgetUid') + '[address]">');
        var nameInput = $('<input type="hidden" name="' + widget.data('widgetUid') + '[name]">');
        var latlngInput = $('<input type="hidden" name="' + widget.data('widgetUid') + '[latlng]">');
        var autocomplete = new google.maps.places.Autocomplete(searchInput[0], {
            types: ['geocode']
        });

        widget.append(addressInput);
        widget.append(nameInput);
        widget.append(latlngInput);
        setBounds(autocomplete);

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
                searchInput.val('');
                addressInput.val('');
                latlngInput.val('');
            }
        });

        google.maps.event.addListener(autocomplete, 'place_changed', function () {
            var place = autocomplete.getPlace();
            if (place.hasOwnProperty('geometry')) {
                addressInput.val(place.formatted_address);
                nameInput.val(place.name);
                latlngInput.val(place.geometry.location.lat() + ',' + place.geometry.location.lng());
            }
        });

        // Initial automatic location detection
        if (!searchInput.val() && navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(function (position) {
                var geoCoder = new google.maps.Geocoder();
                var latLng = new google.maps.LatLng(position.coords.latitude, position.coords.longitude);
                geoCoder.geocode({'latLng': latLng}, function (results, status) {
                    if (status == google.maps.GeocoderStatus.OK && results.length) {
                        var place = results[0];
                        searchInput.val(place.formatted_address);
                        addressInput.val(place.formatted_address);
                        latlngInput.val(place.geometry.location.lat() + ',' + place.geometry.location.lng());
                    }
                });
            });
        }
    });
});