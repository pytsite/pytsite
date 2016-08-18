pytsite.google.maps = {
    ready: false
};

pytsite.google.maps.initCallback = function () {
    pytsite.browser.loadAssets([
        'pytsite.google@js/google-maps-InfoBox.min.js',
        'pytsite.google@js/google-maps-MarkerWithLabel.min.js',
        'pytsite.google@js/google-maps-RichMarker.min.js'
    ]).done(function () {
        $(window).trigger('pytsite.google.maps.ready');
        pytsite.google.maps.ready = true;
    });
};

pytsite.google.maps.Map = function (mapNode, options) {
    var self = this;

    // Options
    self.options = {
        // https://developers.google.com/maps/documentation/javascript/controls
        center: new google.maps.LatLng(50.45, 30.52),
        zoom: 18,

        // PytSite specific options
        mapCenterControl: true,
        mapCenterControlOptions: {
            position: google.maps.ControlPosition.RIGHT_TOP
        },
        currentPositionMarker: false,
        currentPositionMarkerOptions: {},
        directionsService: false,
        directionsRendererOptions: {
            hideRouteList: true
        },
        trackPosition: false,
        trackPositionOptions: {
            onSuccess: null,
            onError: null
        }
    };
    $.extend(true, self.options, options);

    self.mapObject = new google.maps.Map(mapNode, self.options);
    self.mapNode = mapNode;
    self.currentPosition = self.options.center;
    self.markers = [];
    self.infoBoxes = [];
    self.trackPositionCount = 0;

    // Create map center control
    if (self.options.mapCenterControl) {
        // Create and add button
        var btn = $('<a class="pytsite-google-map-control center-map hidden" href="#">' +
            '<i class="fa fa-fw fa-3x fa-crosshairs"></i></a>');
        self.mapObject.controls[google.maps.ControlPosition.RIGHT_TOP].push(btn[0]);

        // Center the map and hide the button after click on it
        btn.click(function (e) {
            e.preventDefault();
            self.setCenterToCurrentPosition();
            if (self.mapCenterControl) {
                self.mapCenterControl.addClass('hidden');
            }
        });
        self.mapCenterControl = btn;

        // Show the button on map dragging
        self.mapObject.addListener('drag', function () {
            if (self.mapCenterControl) {
                self.mapCenterControl.removeClass('hidden');
            }
        });
    }

    // Create current position marker
    if (self.options.currentPositionMarker) {
        $.extend(self.options.currentPositionMarkerOptions, {
            position: self.currentPosition,
            map: self.mapObject
        });
        self.currentPositionMarker = new google.maps.Marker(self.options.currentPositionMarkerOptions);
    }

    // Setup directions service
    if (self.options.directionsService) {
        self.directionsService = new google.maps.DirectionsService();
        self.directionsRenderer = new google.maps.DirectionsRenderer(self.directionsRendererOptions);
    }

    // Setup position change listener
    if (self.options.trackPosition) {
        if (!('geolocation' in navigator))
            throw 'You browser does not support geolocation';

        navigator.geolocation.watchPosition(
            function (position) {
                // Update current position data structure
                self.currentPosition = new google.maps.LatLng(position.coords.latitude, position.coords.longitude);

                // Update current position marker
                if (self.currentPositionMarker) {
                    self.currentPositionMarker.setPosition(self.currentPosition);
                }

                // Call onSuccess() callback
                if (self.options.trackPositionOptions.onSuccess) {
                    self.options.trackPositionOptions.onSuccess(position, self.trackPositionCount);
                }

                // Move center to the current position
                if (self.options.mapCenterControl && self.mapCenterControl.hasClass('hidden')) {
                    self.setCenterToCurrentPosition();
                }

                ++self.trackPositionCount;
            }, function (err) {
                // Call onError() callback
                if (self.options.trackPositionOptions.onError) {
                    self.options.trackPositionOptions.onError(err);
                }
            }, {
                enableHighAccuracy: true
            }
        );
    }

    /**
     * Center map to its current position.
     */
    self.setCenterToCurrentPosition = function () {
        self.mapObject.setCenter(self.currentPosition);

        if (self.options.mapCenterControl) {
            self.mapCenterControl.addClass('hidden');
        }
    };

    /**
     * Adjusts map viewport to make all markers visible.
     */
    self.fitBounds = function () {
        var markerBounds = new google.maps.LatLngBounds();
        markerBounds.extend(self.currentPositionMarker.getPosition());

        for (var i = 0; i < self.markers.length; ++i) {
            markerBounds.extend(self.markers[i].getPosition());
        }

        self.mapObject.fitBounds(markerBounds);
        if (self.mapObject.getZoom() > self.options.zoom)
            self.mapObject.setZoom(self.options.zoom);
    };

    /**
     * Update current coordinates.
     */
    self.updateCurrentPosition = function () {
        var defer = $.Deferred();

        if (!('geolocation' in navigator)) {
            defer.reject('You browser does not support geolocation');
            throw 'You browser does not support geolocation';
        }

        navigator.geolocation.getCurrentPosition(function (position) {
            self.currentPosition = new google.maps.LatLng(position.coords.latitude, position.coords.longitude);
            defer.resolve(position);
        }, function (err) {
            console.error(err);
            defer.reject(err);
        }, {
            enableHighAccuracy: true
        });

        return defer;
    };

    /**
     * Clear drawn routes.
     */
    self.clearRoutes = function () {
        if (self.options.directionsService) {
            self.directionsRenderer.setMap(null);
        }
    };

    /**
     * Draw a route.
     */
    self.drawRoute = function (origin, destination, travelMode) {
        var request = {
            origin: origin,
            destination: destination,
            travelMode: travelMode
        };

        // Making request to Google Directions Service
        self.directionsService.route(request, function (result, status) {
            if (status == google.maps.DirectionsStatus.OK) {
                self.directionsRenderer.setMap(self.mapObject);
                self.directionsRenderer.setDirections(result);
            }
            else {
                alert('Error while drawing route: ' + status);
            }
        });
    };

    /**
     * Create and add simple marker.
     *
     * @see https://developers.google.com/maps/documentation/javascript/markers
     */
    self.addMarker = function(position, title, icon) {
        var opts = {
            position: position,
            title: title,
            icon: icon,
            map: self.mapObject
        };

        var marker = new google.maps.Marker(opts);
        self.markers.push(marker);

        return marker;
    };

    /**
     * Create and add marker with label.
     *
     * @see https://github.com/printercu/google-maps-utility-library-v3-read-only/tree/master/markerwithlabel
     */
    self.addMarkerWithLabel = function (position, markerOpts) {
        var opts = {
            position: position,
            map: self.mapObject
        };

        $.extend(opts, markerOpts);

        var marker = new MarkerWithLabel(opts);
        self.markers.push(marker);

        return marker;
    };

    // === Create info box ===
    // https://github.com/printercu/google-maps-utility-library-v3-read-only/tree/master/infobox
    self.createInfoBox = function (boxOpts) {
        var iBox = new InfoBox(boxOpts);
        self.infoBoxes.push(iBox);

        return iBox;
    };

    // === Close all info boxes ===
    self.closeInfoBoxes = function () {
        for (var i = 0; i < self.infoBoxes.length; ++i) {
            self.infoBoxes[i].close();
        }
    };

    // Reset map
    self.reset = function () {
        // Clear drawn routes
        self.clearRoutes();

        // Close all info windows before markers deletion
        self.closeInfoBoxes();

        // Detach markers from the map
        for (var i = 0; i < self.markers.length; ++i) {
            self.markers[i].setMap(null);
        }

        self.markers = [];
    };
};
