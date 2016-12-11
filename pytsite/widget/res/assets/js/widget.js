pytsite.widget = {
    Widget: function (em) {
        var self = this;
        self.em = em = $(em);
        self.cid = em.data('cid');
        self.uid = em.data('uid');
        self.replaces = em.data('replaces');
        self.formArea = em.data('formArea');
        self.formStep = em.data('formStep');
        self.parentUid = em.data('parentUid');
        self.alwaysHidden = em.data('hidden') == 'True';
        self.weight = em.data('weight');
        self.assets = em.data('assets') ? self.em.data('assets') : [];
        self.messagesEm = em.find('.widget-messages').first();
        self.childWidgets = {};

        // Clear state fo the widget
        self.clearState = function () {
            self.em.removeClass('has-success');
            self.em.removeClass('has-warning');
            self.em.removeClass('has-error');

            return self;
        };

        // Set state of the widget
        self.setState = function (type) {
            self.clearState();
            self.em.addClass('has-' + type);

            return self;
        };

        // Clear messages of the widget
        self.clearMessages = function () {
            if (self.messagesEm.length)
                self.messagesEm.html('');

            return self;
        };

        // Add message to the widget
        self.addMessage = function (msg) {
            if (self.messagesEm.length)
                self.messagesEm.append('<span class="help-block">{0}</span>'.format(msg));

            return self;
        };

        // Hide the widget
        self.hide = function () {
            self.em.addClass('hidden');

            return self;
        };

        // Show the widget
        self.show = function () {
            if (!self.alwaysHidden)
                self.em.removeClass('hidden');

            return self;
        };

        // Load children widgets
        if (self.em.data('container') == 'True') {
            self.em.find('> .pytsite-widget:not(.initialized)').each(function () {
                var w = new pytsite.widget.Widget(this);
                self.childWidgets[w.uid] = w;
            });
        }

        // Load widget's assets
        pytsite.browser.loadAssets(self.assets).done(function () {
            // Initialize the widget
            $(window).trigger('pytsite.widget.init:' + self.cid, [self]);
            $(self).trigger('ready', [self]);
            self.em.addClass('initialized');
        }).fail(function () {
            $(self).trigger('initError', [self]);
        });
    }
};

$(function () {
    // Initialize all widgets found on a page
    $('.pytsite-widget').not('.initialized').each(function () {
        new pytsite.widget.Widget(this);
    });
});
