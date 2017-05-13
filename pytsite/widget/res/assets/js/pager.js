define(['jquery', 'pytsite-http-api', 'pytsite-lang'], function ($, httpApi, lang) {
    return function (widget) {
        var em = widget.em;
        var httpApiEp = em.data('httpApiEp');

        if (!httpApiEp)
            return;

        var buttons = em.find('li');
        var totalItems = parseInt(em.data('totalItems'));
        var currentPage = parseInt(em.data('currentPage'));
        var totalPages = parseInt(em.data('totalPages'));
        var perPage = parseInt(em.data('perPage'));
        var visibleNumbers = parseInt(em.data('visibleNumbers'));

        /**
         * Make an HTTP API request.
         *
         * @param pageNum
         */
        function loadData(pageNum) {
            var skip = (pageNum - 1) * perPage;
            if (skip < 0)
                skip = 0;

            httpApi.get(httpApiEp, {
                skip: skip,
                count: perPage
            }).done(function (r) {
                $(window).trigger('pytsite.widget.select.pager.httpApiLoad', [r, pageNum, widget]);
            }).fail(function (r) {
                $(window).trigger('pytsite.widget.select.pager.httpApiError', [r, pageNum, widget]);
            });
        }

        /**
         * Renumber buttons.
         */
        function renumber(firstNum) {
            for (var i = 0; i < visibleNumbers; i++) {
                var k = firstNum + i;

                var btn = $(buttons.filter('.page').get(i));
                btn.attr('data-page', k);

                var btnA = btn.find('a');
                btnA.text(k);
                btnA.attr('title', lang.t('pytsite.widget@page_num', {num: k}));
                btnA.attr('href', btnA.attr('href').replace(/page=\d+/, 'page=' + k))
            }
        }

        /**
         * Refresh state.
         */
        function refresh() {
            var firstVisibleNum = parseInt(buttons.filter('.page').first().attr('data-page'));
            var lastVisibleNum = parseInt(buttons.filter('.page').last().attr('data-page'));

            if (currentPage < firstVisibleNum) {
                renumber(currentPage);
            }
            else if (currentPage > lastVisibleNum) {
                renumber(currentPage - visibleNumbers + 1);
            }

            em.find('li').removeClass('active');
            em.find('li[data-page="' + currentPage + '"]').addClass('active');

            em.attr('data-current-page', currentPage);
            loadData(currentPage);
        }

        /**
         * Click on the button handler.
         */
        buttons.click(function (e) {
            e.preventDefault();

            var btn = $(this);

            if (btn.hasClass('active')) {
                return;
            }
            else if (btn.hasClass('first-page')) {
                if (currentPage === 1)
                    return;

                currentPage = 1;
            }
            else if (btn.hasClass('previous-page')) {
                if (currentPage === 1)
                    return;

                --currentPage;
            }
            else if (btn.hasClass('next-page')) {
                if (currentPage === totalPages)
                    return;

                ++currentPage;
            }
            else if (btn.hasClass('last-page')) {
                if (currentPage === totalPages)
                    return;

                currentPage = totalPages;
            }
            else {
                currentPage = parseInt(btn.attr('data-page'));
            }

            refresh();
        });

        // Init
        loadData(currentPage);
    }
});
