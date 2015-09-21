pytsite.responsive = function () {
    $('div.pytsite-img').each(function () {
        var cont = $(this);
        var img_path = cont.data('path');
        var img_alt = cont.data('alt');


        if (typeof img_path == 'undefined')
            return null;

        if (typeof img_alt == 'undefined')
            img_alt = '';

        var parent_cont = $(cont).parent();
        while (true) {
            if (parent_cont.width() > 0) {
                cont.replaceWith(function () {
                    img_path = '/image/resize/' + parent_cont.width() + '/0/' + img_path;
                    return '<img class="img-responsive pytsite-img" src="' + img_path + '" alt="' + img_alt + '">';
                });

                break;
            }

            parent_cont = parent_cont.parent();
        }
    });
};

$(function () {
    pytsite.responsive();
});
