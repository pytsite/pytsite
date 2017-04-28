require(['jquery', 'cookie', 'assetman', 'twitter-bootstrap'], function ($, cookie, assetman) {
    assetman.loadJS('pytsite.admin@AdminLTE/js/app.js');

    $('.sidebar-toggle').click(function () {
        if ($('body').hasClass('sidebar-collapse'))
            cookie.remove('adminSidebarCollapsed');
        else
            cookie.set('adminSidebarCollapsed', '1', {expires: 3650});
    });
});
