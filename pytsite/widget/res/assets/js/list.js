$(window).on('pytsite.widget.init:pytsite.widget._input.List', function (e, widget) {
    function countSlots(w) {
        var n = 0;
        w.find('.slot').each(function () {
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
                    w.find('.add-btn a').show();
            }
            else
                w.find('.slot').first().find('input').val('');
        });
    }

    var maxValues = parseInt(widget.data('maxValues'));
    var slots = widget.find('.slots');
    var addBtn = widget.find('.add-btn a');

    if (countSlots(widget) >= maxValues)
        addBtn.hide();

    widget.find('.slot').each(function () {
        setupSlot(widget, $(this), maxValues);
    });

    addBtn.click(function (e) {
        e.preventDefault();

        if (countSlots(widget) >= maxValues)
            return false;

        var btn = $(this);
        var slot = widget.find('.slot').first().clone();

        slot.find('input').val('');
        slots.append(slot);
        setupSlot(widget, slot, maxValues);
        if (countSlots(widget) >= maxValues)
            btn.hide();
    });

});
