$(function() {
    $('.odm-ui-browser').each(function() {
        var browser = $(this);
        var massDeleteButton = browser.find('.mass-delete-button');

        var getCheckedIds = function() {
            var r = [];
            browser.find('[name=btSelectItem]:checked').each(function() {
                r.push($(this).closest('tr').find('.entity-actions').first().data('entityId'))
            });

            return r;
        };

        massDeleteButton.click(function(e) {
            e.preventDefault();
            var ids = getCheckedIds();
            if(ids.length)
                window.location.href = $(this).attr('href') + '?' + $.param({ids: ids});
        });
    });
});