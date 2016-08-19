$(function () {
    $('.sidebar-toggle').click(function () {
        if ($('body').hasClass('sidebar-collapse'))
            Cookies.remove('adminSidebarCollapsed');
        else
            Cookies.set('adminSidebarCollapsed', '1', {expires: 3650});
    });
});
