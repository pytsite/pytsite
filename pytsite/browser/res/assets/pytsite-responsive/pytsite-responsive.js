define(['jquery'], function ($) {
    // Align image's side length
    function _align_length(l) {
        if (l <= 0)
            return l;

        var max = 2000;
        var step = 50;
        for (var i = 0; i <= max; i += step) {
            if (l <= i)
                return i;
        }

        return l;
    }

    // Searches for closest container with non-zero width
    function _getParentWidth(child) {
        var parent_cont = $(child).parent();
        var tries = 0;
        var maxTries = 10;
        while (true) {
            var parentTag = parent_cont.prop('tagName');
            if (parent_cont.width() > 0 && (parentTag === 'P' || parentTag === 'DIV'))
                return parent_cont.width();

            ++tries;

            if (tries >= maxTries)
                return parent_cont.width();

            parent_cont = parent_cont.parent();
        }
    }

    function _getImgResponsiveUrl(cont) {
        var fullSizeUrl = cont.data('url');
        if (fullSizeUrl === undefined)
            fullSizeUrl = cont.data('responsive-bg-url');

        var enlarge = cont.data('enlarge') === 'True';
        var aspectRatio = cont.data('aspectRatio');
        var origWidth = parseInt(cont.data('width'));
        var parentContainerWidth = _getParentWidth(cont);
        var newWidth = origWidth;
        var newHeight = 0;

        // If enlarging is necessary
        if (origWidth < parentContainerWidth) {
            if (enlarge)
                newWidth = _align_length(parentContainerWidth);
        }
        else {
            newWidth = _align_length(parentContainerWidth);
        }

        // If aspect ratio was specified
        if (aspectRatio !== undefined && aspectRatio !== 'None')
            newHeight = _align_length(parseInt(newWidth / parseFloat(aspectRatio)));

        return fullSizeUrl.replace('/0/0/', '/' + newWidth + '/' + newHeight + '/');
    }

    function _getImgElement(cont) {
        var imgUrl = cont.data('url');
        var alt = cont.data('alt');
        var enlarge = cont.data('enlarge');
        var css = cont.attr('class');
        var orig_width = parseInt(cont.data('width'));
        var orig_height = parseInt(cont.data('height'));
        var aspect_ratio = cont.data('aspectRatio');
        var src = _getImgResponsiveUrl(cont);

        return '<img class="' + css + '" src="' + src + '" alt="' + alt + '" data-url="' + imgUrl + '"' +
            ' data-alt="' + alt + '" data-aspect-ratio="' + aspect_ratio + '"' + ' data-enlarge="' + enlarge + '"' +
            ' data-width="' + orig_width + '"' + ' data-height="' + orig_height + '"' + '>';
    }

    function responsiveImages(selector) {
        if (typeof selector === 'undefined')
            selector = 'span.pytsite-img';

        // Set images
        $(selector).each(function () {
            $(this).replaceWith(function () {
                return _getImgElement($(this));
            });
        });

        // Set background images
        $('[data-responsive-bg-url]').each(function () {
            $(this).css('background-image', 'url(' + _getImgResponsiveUrl($(this)) + ')');
        });
    }

    function responsiveIframes(selector) {
        if (typeof selector === 'undefined')
            selector = 'iframe';

        $(selector).each(function () {
            var origWidth = parseInt($(this).width());
            var origHeight = parseInt($(this).height());
            var newWidth = _getParentWidth(this);
            var aspect = origWidth / origHeight;
            var newHeight = newWidth / aspect;
            $(this).attr('width', newWidth);
            $(this).attr('height', newHeight);
        });
    }

    function responsiveAll(imagesSelector, iframesSelector) {
        responsiveImages(imagesSelector);
        responsiveIframes(iframesSelector);
    }

    // Automatically process all images and iframes found in DOM right after DOM is ready
    responsiveAll();

    return {
        images: responsiveImages,
        iframes: responsiveIframes,
        all: responsiveAll
    }
});
