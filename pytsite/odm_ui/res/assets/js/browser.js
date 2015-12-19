$(function() {
    $('.odm-ui-browser').each(function() {
        var browser = $(this);
        var massActionButtons = browser.find('.mass-action-button');
        var form = browser.find('form').first();

        var getCheckedIds = function() {
            var r = [];
            browser.find('[name=btSelectItem]:checked').each(function() {
                r.push($(this).closest('tr').find('.entity-actions').first().data('entityId'))
            });

            return r;
        };

        function updateMassActionButtons() {
            if (browser.find('[name=btSelectItem]:checked').length)
                massActionButtons.removeClass('hidden');
            else
                massActionButtons.addClass('hidden');
        }

        massActionButtons.click(function(e) {
            e.preventDefault();

            var ids = getCheckedIds();
            if(ids.length) {
                form.prop('action', $(this).attr('href'));

                $(ids).each(function(k, v) {
                    form.append($('<input type="hidden" name="ids[]" value="' + v + '">'));
                });

                form.submit();
            }
        });

        // Disable unnecessary checkboxes
        browser.on('load-success.bs.table', function(e, data) {
            browser.find('.entity-actions.empty').each(function() {
                $(this).closest('tr').find('.bs-checkbox input[type=checkbox]').attr('disabled', 'disabled');
            });
        });

        // Show/hide mass action buttons
        updateMassActionButtons();
        browser.on('check.bs.table', updateMassActionButtons);
        browser.on('uncheck.bs.table', updateMassActionButtons);
        browser.on('check-all.bs.table', updateMassActionButtons);
        browser.on('uncheck-all.bs.table', updateMassActionButtons);
    });
});
