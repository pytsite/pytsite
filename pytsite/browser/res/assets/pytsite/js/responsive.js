pytsite.responsive = function () {
    // Align image's side length
    function align_length(l) {
        if (l <= 0)
            return l;

        var max = 2000;
        var step = 50;
        for(var i = 0; i <= max; i += step) {
            if (l <= i)
                return i;
        }

        return l;
    }

    // Searches for closest container with non-zero width
    function getParentWidth(child) {
        var parent_cont = $(child).parent();
        var tries = 0;
        var maxTries = 10;
        while (true) {
            var parentTag = parent_cont.prop('tagName');
            if (parent_cont.width() > 0 && (parentTag == 'P' || parentTag == 'DIV'))
                return parent_cont.width();

            ++tries;

            if (tries >= maxTries)
                return parent_cont.width();

            parent_cont = parent_cont.parent();
        }
    }

    function getImgContainer(cont) {
        var img_path = cont.data('path');
        if (typeof img_path == 'undefined')
            return cont;

        var alt = cont.data('alt');
        var enlarge = cont.data('enlarge');
        var css = cont.attr('class');
        var orig_width = parseInt(cont.data('width'));
        var orig_height = parseInt(cont.data('height'));
        var new_width = align_length(getParentWidth(cont));
        var new_height = 0;

        var aspect_ratio = cont.data('aspectRatio');
        if (aspect_ratio != 'None')
            new_height = align_length(parseInt(new_width / parseFloat(aspect_ratio)));

        var src = '/image/resize/0/' + new_height + '/' + img_path;
        if (enlarge == 'True' || new_width <= orig_width)
            src = '/image/resize/' + new_width + '/' + new_height + '/' + img_path;

        return '<img class="' + css + '" src="' + src + '" alt="' + alt + '" data-path="' + img_path + '"' +
            'data-alt="' + alt + '" data-aspect-ratio="' + aspect_ratio + '"' + 'data-enlarge="' + enlarge + '"' +
            'data-width="' + orig_width + '"' + 'data-height="' + orig_height + '"' + '>';
    }

    // Replace images
    $('img.pytsite-img,span.pytsite-img').each(function () {
        $(this).replaceWith(function () {
            return getImgContainer($(this));
        });
    });

    // Replace iframes
    $('iframe').each(function() {
        var origWidth = parseInt($(this).width());
        var origHeight = parseInt($(this).height());
        var newWidth = getParentWidth(this);
        var aspect = origWidth / origHeight;
        var newHeight = newWidth / aspect;
        $(this).attr('width', newWidth);
        $(this).attr('height', newHeight);
    });
};

$(function () {
    pytsite.responsive();

    $(window).resize($.debounce(1000, pytsite.responsive));
});
