$(window).on('pytsite.widget.init:pytsite.widget._select.Pager', function (e, widget) {
    var em = widget.em;
    var ajax = em.data('ajax');
    if (!ajax)
        return;

    var buttons = em.find('a');
    var perPage = parseInt(em.data('perPage'));

    function loadData(pageNum) {
        var skip = (pageNum - 1) * perPage;
        if (skip < 0)
            skip = 0;

        pytsite.httpApi.get(ajax, {
            skip: skip,
            count: perPage
        }).done(function (r) {
            $(window).trigger('pytsite.widget.select.pager.load', [r, pageNum, widget]);
        }).fail(function (r) {
            $(window).trigger('pytsite.widget.select.pager.error', [r, pageNum, widget]);
        });
    }

    buttons.click(function (e) {
        e.preventDefault();

        var btn = $(this);
        var li = btn.closest('li');

        if (li.hasClass('active'))
            return;

        em.find('li').removeClass('active');
        li.addClass('active');

        loadData(parseInt(btn.data('page')));
    });

    // Initial data load
    loadData(parseInt(em.data('currentPage')));
});
