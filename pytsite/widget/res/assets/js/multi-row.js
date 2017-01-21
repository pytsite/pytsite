function pytsiteWidgetMultiRowSetupSlot(i, em, slotsHeader, slotsContainer) {
    em.find('.order-col').html('[' + (i + 1) + ']');

    // Show/hide slots header
    if (slotsContainer.find('.slot').length == 1)
        slotsHeader.addClass('hidden');
    else
        slotsHeader.removeClass('hidden');

    // Set unique ID for each input
    em.find('input,select,textarea').each(function() {
        var origId = $(this).attr('id');
        if (origId) {
            $(this).attr('id', origId + '-' + i);
        }
    });

    em.find('.button-remove-slot').click(function (e) {
        e.preventDefault();

        em.remove();

        if (slotsContainer.find('.slot').length == 1)
            slotsHeader.addClass('hidden');
        else
            slotsHeader.removeClass('hidden');

        // Renumber slots
        slotsContainer.find('.slot:not(.sample)').each(function (i, em) {
            $(em).find('.order-col').html('[' + (i + 1) + ']');
        });
    });
}

$(window).on('pytsite.widget.init:pytsite.widget._base.MultiRow', function (e, widget) {
    var slotsHeader = widget.em.find('.slots-header');
    var slotsContainer = widget.em.find('.slots');
    var slots = widget.em.find('.slot');

    // Clone and setup sample slot
    var baseSlot = slots.filter('.sample').clone();
    baseSlot.removeClass('sample hidden');

    // Setup each existing slot
    slots.filter(':not(.sample)').each(function (i, em) {
        pytsiteWidgetMultiRowSetupSlot(i, $(em), slotsHeader, slotsContainer);
    });

    widget.em.find('.button-add-slot').click(function (e) {
        e.preventDefault();

        var newSlot = baseSlot.clone();
        slotsContainer.append(newSlot);
        pytsiteWidgetMultiRowSetupSlot(slotsContainer.find('.slot').length - 2, newSlot, slotsHeader, slotsContainer)
    });
});
