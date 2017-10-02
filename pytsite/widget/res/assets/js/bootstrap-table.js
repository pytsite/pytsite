define(['jquery', 'twitter-bootstrap-table'], function ($) {
    function init(widget) {
        var widgetEm = widget.em;
        var massActionButtons = widgetEm.find('.mass-action-button');
        var form = widgetEm.closest('form');

        var getCheckedIds = function () {
            var r = [];
            widgetEm.find('[name=btSelectItem]:checked').each(function () {
                r.push($(this).closest('tr').find('.entity-actions').first().data('entityId'))
            });

            return r;
        };

        function updateMassActionButtons() {
            if (widgetEm.find('[name=btSelectItem]:checked').length) {
                // Show mass action buttons if at least one checkbox is selected
                massActionButtons.removeClass('hidden');
            }

            else {
                // Hide otherwise
                massActionButtons.addClass('hidden');
            }
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
        widgetEm.on('load-success.bs.table', function (e, data) {
            widgetEm.find('.entity-actions.empty').each(function () {
                $(this).closest('tr').find('.bs-checkbox input[type=checkbox]').attr('disabled', 'disabled');
            });
        });

        // Show and initialize table
        widgetEm.find('table').removeClass('hidden').bootstrapTable();

        // Show/hide mass action buttons
        updateMassActionButtons();
        widgetEm.on('check.bs.table', updateMassActionButtons);
        widgetEm.on('uncheck.bs.table', updateMassActionButtons);
        widgetEm.on('check-all.bs.table', updateMassActionButtons);
        widgetEm.on('uncheck-all.bs.table', updateMassActionButtons);
    }

    return init;
});
