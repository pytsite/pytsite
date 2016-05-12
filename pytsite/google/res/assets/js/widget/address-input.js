$(window).on('pytsite.widget.init:pytsite.google._maps._widget.AddressInput', function (e, widget) {
    function setBounds(autcomplete) {
        if ('geolocation' in navigator) {
            navigator.geolocation.updateCurrentPosition(function (position) {
                var geolocation = new google.maps.LatLng(position.coords.latitude, position.coords.longitude);
                var circle = new google.maps.Circle({center: geolocation, radius: position.coords.accuracy});

                autcomplete.setBounds(circle.getBounds());
            });
        }
    }

    function init() {
        var uid = widget.em.data('uid');
        var searchInput = widget.em.find('input[name="' + uid + '[search]"]');
        var addressInput = widget.em.find('input[name="' + uid + '[address]"]');
        var lngInput = widget.em.find('input[name="' + uid + '[lng]"]');
        var latInput = widget.em.find('input[name="' + uid + '[lat]"]');
        var componentsInput = widget.em.find('input[name="' + uid + '[address_components]"]');
        var autocomplete = new google.maps.places.Autocomplete(searchInput[0], {
            types: ['geocode']
        });

        widget.em.keydown(function (event) {
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

        widget.update = function() {
            setBounds(autocomplete);
            navigator.geolocation.updateCurrentPosition(function (position) {
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
        };

        // Automatic location detection
        if (widget.em.data('autodetect') == 'True') {
            widget.update();
            setInterval(widget.update, 10000)
        }
    }

    // Start work only after Google libraries are all ready
    if (pytsite.google.ready)
        init();
    else
        $(window).on('pytsite.google.ready', init);
});
