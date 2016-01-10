pytsite.responsive = {
    init: function () {
        var image_containers = $('span.pytsite-img');

        image_containers.each(function () {
            var cont = $(this);
            var img_path = cont.data('path');
            var img_alt = cont.data('alt').replace(/"/g, '&quot;');
            var aspect_ratio = null;

            if (cont.data('aspectRatio') != 'None')
                aspect_ratio = parseFloat(cont.data('aspectRatio'));

            if (typeof img_path == 'undefined')
                return null;

            if (typeof img_alt == 'undefined')
                img_alt = '';

            var parent_cont = $(cont).parent();
            while (true) {
                // Search for container with non-zero width
                if (parent_cont.width() > 0) {
                    var width = parent_cont.width();
                    var height = 0;

                    if (aspect_ratio)
                        height = parseInt(width / aspect_ratio);

                    cont.replaceWith(function () {
                        img_path = '/image/resize/' + width + '/' + height + '/' + img_path;
                        return '<img class="' + cont.attr('class') + '" src="' + img_path + '" alt="' + img_alt + '">';
                    });

                    break;
                }

                parent_cont = parent_cont.parent();
            }
        });
    }
};


$(function () {
    pytsite.responsive.init();
});
