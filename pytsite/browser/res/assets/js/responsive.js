pytsite.responsive = function () {
    // Searches for closest container with non-zero width
    function get_parent_width(child) {
        var parent_cont = $(child).parent();
        while (true) {
            if (parent_cont.width() > 0)
                return parent_cont.width();

            parent_cont = parent_cont.parent();
        }
    }

    function get_img_container(cont) {
        var img_path = cont.data('path');
        if (typeof img_path == 'undefined')
            return cont;

        var alt = cont.data('alt');
        var css = cont.attr('class');
        var width = get_parent_width(cont);
        var height = 0;

        var aspect_ratio = cont.data('aspectRatio');
        if (aspect_ratio != 'None')
            height = parseInt(width / parseFloat(aspect_ratio));

        var src = '/image/resize/' + width + '/' + height + '/' + img_path;
        return '<img class="' + css + '" src="' + src + '" alt="' + alt + '" data-path="' + img_path + '"' +
            'data-alt="' + alt + '" data-aspect-ratio="' + aspect_ratio + '">';
    }

    $('img.pytsite-img,span.pytsite-img').each(function () {
        $(this).replaceWith(function () {
            return get_img_container($(this));
        });
    });
};

$(function () {
    pytsite.responsive();

    $(window).resize($.debounce(1000, pytsite.responsive));
});
