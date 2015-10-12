$(function() {
    // Smooth scrolling init
    var platform = navigator.platform.toLowerCase();
    if (platform.indexOf('win') == 0 || platform.indexOf('linux') == 0) {
        if (navigator.userAgent.indexOf('WebKit') > 0) {
            $.srSmoothscroll();
        }
    }
});
