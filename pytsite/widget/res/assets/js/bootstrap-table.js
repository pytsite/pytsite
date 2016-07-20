$(window).on('pytsite.widget.init:pytsite.widget._misc.BootstrapTable', function (e, widget) {
    var browser = widget.em;
    var massActionButtons = browser.find('.mass-action-button');
    var form = browser.closest('form');

    var getCheckedIds = function () {
        var r = [];
        browser.find('[name=btSelectItem]:checked').each(function () {
            r.push($(this).closest('tr').find('.entity-actions').first().data('entityId'))
        });

        return r;
    };

    function updateMassActionButtons() {
        if (browser.find('[name=btSelectItem]:checked').length)
            // Show mass action buttons if at least one checkbox is selected
            massActionButtons.removeClass('hidden');
        else
            // Hide otherwise
            massActionButtons.addClass('hidden');
    }

    massActionButtons.click(function (e) {
        e.preventDefault();

        var ids = getCheckedIds();
        if (ids.length) {
            form.prop('action', $(this).attr('href'));

            $(ids).each(function (k, v) {
                form.append($('<input type="hidden" name="ids[]" value="' + v + '">'));
            });

            form.submit();
        }
    });

    // Disable unnecessary checkboxes
    browser.on('load-success.bs.table', function (e, data) {
        browser.find('.entity-actions.empty').each(function () {
            $(this).closest('tr').find('.bs-checkbox input[type=checkbox]').attr('disabled', 'disabled');
        });
    });

    browser.find('table').bootstrapTable().removeClass('hidden');

    // Show/hide mass action buttons
    updateMassActionButtons();
    browser.on('check.bs.table', updateMassActionButtons);
    browser.on('uncheck.bs.table', updateMassActionButtons);
    browser.on('check-all.bs.table', updateMassActionButtons);
    browser.on('uncheck-all.bs.table', updateMassActionButtons);
});
