pytsite.widget = {
    Widget: function (em) {
        var self = this;
        self.em = $(em);
        self.cid = self.em.data('cid');
        self.uid = self.em.data('uid');
        self.replaces = self.em.data('replaces');
        self.formArea = self.em.data('formArea');
        self.formStep = self.em.data('formStep');
        self.alwaysHidden = self.em.data('hidden') == 'True';
        self.weight = self.em.data('weight');
        self.assets = self.em.data('assets') ? self.em.data('assets') : [];
        self.messagesEm = $('<div class="messages">');
        self.childWidgets = {};

        // Add block for messages
        var fGroup = self.em.find('.form-group').first();
        if (fGroup.length)
            fGroup.append(self.messagesEm);
        else
            self.em.append(self.messagesEm);

        // Load children widgets
        if (self.em.data('container') == 'True') {
            self.em.find('.children .pytsite-widget:not(.initialized)').each(function () {
                var w = pytsite.widget.Widget(this);
                self.childWidgets[w.uid] = w;
            });
        }

        // Load widget's assets
        pytsite.browser.addAssets(self.assets);

        // Initialize the widget
        $(window).trigger('pytsite.widget.init:' + self.cid, [self.em, self]);
        self.em.addClass('initialized');

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
            self.messagesEm.html('');

            return self;
        };

        // Add message to the widget
        self.addMessage = function (msg) {
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
    }
};

// Automatically initialize all existing widgets after page load
$(function () {
    $('.pytsite-widget:not(.initialized)').each(function () {
        pytsite.widget.Widget(this);
    });
});
