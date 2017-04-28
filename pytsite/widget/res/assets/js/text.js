define(function () {
    return function (widget) {
        widget.em.find('input').focus(function () {
            this.select();
        });
    }
});
