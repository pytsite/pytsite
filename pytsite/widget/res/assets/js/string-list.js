define(['jquery', 'assetman'], function ($, assetman) {
    return function (widget) {
        function countSlots(w) {
            var n = 0;
            w.em.find('.slot').each(function () {
                $(this).find('.order').text('[' + ++n + ']');
            });

            return n;
        }

        function setupSlot(w, slot, maxSlots) {
            slot.find('.delete-btn a').click(function (e) {
                e.preventDefault();

                if (countSlots(w) > 1) {
                    slot.remove();
                    if (countSlots(w) < maxSlots)
                        w.em.find('.add-btn a').show();
                }
                else
                    w.em.find('.slot').first().find('input').val('');
            });
        }

        var maxValues = parseInt(widget.em.data('maxValues'));
        var slots = widget.em.find('.slots');
        var addBtn = widget.em.find('.add-btn a');

        assetman.loadCSS('pytsite.widget@css/string-list.css');

        if (countSlots(widget) >= maxValues)
            addBtn.hide();

        widget.em.find('.slot').each(function () {
            setupSlot(widget, $(this), maxValues);
        });

        addBtn.click(function (e) {
            e.preventDefault();

            if (countSlots(widget) >= maxValues)
                return false;

            var btn = $(this);
            var slot = widget.em.find('.slot').first().clone();

            slot.find('input').val('');
            slots.append(slot);
            setupSlot(widget, slot, maxValues);
            if (countSlots(widget) >= maxValues)
                btn.hide();
        });
    }
});
