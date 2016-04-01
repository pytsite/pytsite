$(window).on('pytsite.widget.init', function (e, widget) {
    function countSlots(widget) {
        var n = 0;
        widget.find('.slot').each(function () {
            $(this).find('.order').text('[' + ++n + ']');
        });

        return n;
    }

    function setupSlot(widget, slot, maxSlots) {
        slot.find('.delete-btn a').click(function (e) {
            e.preventDefault();

            if (countSlots(widget) > 1) {
                slot.remove();
                if (countSlots(widget) < maxSlots)
                    widget.find('.add-btn a').show();
            }
            else
                widget.find('.slot').first().find('input').val('');
        });
    }

    widget.em.find('.widget-string-list').each(function () {
        var w = $(this);
        var maxValues = parseInt(w.data('maxValues'));
        var slots = w.find('.slots');
        var addBtn = w.find('.add-btn a');

        if (countSlots(w) >= maxValues)
            addBtn.hide();

        w.find('.slot').each(function () {
            setupSlot(w, $(this), maxValues);
        });

        addBtn.click(function (e) {
            e.preventDefault();

            if (countSlots(w) >= maxValues)
                return false;

            var btn = $(this);
            var slot = w.find('.slot').first().clone();

            slot.find('input').val('');
            slots.append(slot);
            setupSlot(w, slot, maxValues);
            if (countSlots(w) >= maxValues)
                btn.hide();
        });
    });
});
