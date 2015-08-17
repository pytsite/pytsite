$(function () {
    $('.widget.geo.location').each(function () {
        var widget = $(this);

        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(function (position) {
                console.log(position);
            });
        }
    });
});