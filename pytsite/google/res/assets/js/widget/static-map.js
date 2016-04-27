function pytsiteGoogleMapsStaticMap(em) {
    var imgUrl = em.data('imgUrl');
    var link = em.data('link');
    var linkTarget = em.data('linkTarget');
    var width = parseInt(em.parent().width());
    var height = width;
    var img = $('<img src="' + imgUrl + '&size=' + width + 'x' + height + '">');

    em.find('a,img').remove();

    if (link != undefined) {
        var a = $('<a href="' + link + '" target="' + linkTarget + '">');
        a.append(img);
        em.append(a);
    }
    else
        em.append(img);
}

$(window).on('pytsite.widget.init:pytsite.google._maps._widget.StaticMap', function (e, widget) {
    pytsiteGoogleMapsStaticMap(widget.em);
    $(window).resize($.debounce(1000, function() {
        pytsiteGoogleMapsStaticMap(widget.em);
    }));
});
