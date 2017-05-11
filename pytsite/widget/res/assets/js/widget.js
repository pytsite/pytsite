define(['jquery'], function ($) {
    /**
     * Widget constructor.
     *
     * @param em
     * @constructor
     */
    function Widget(em) {
        var self = this;
        self.em = em = $(em);
        self.cid = em.data('cid');
        self.uid = em.data('uid');
        self.replaces = em.data('replaces');
        self.formArea = em.data('formArea');
        self.parentUid = em.data('parentUid');
        self.alwaysHidden = em.data('hidden') === 'True';
        self.weight = em.data('weight');
        self.jsModule = em.data('jsModule') ? em.data('jsModule') : [];
        self.messagesEm = em.find('.widget-messages').first();
        self.children = {};

        /**
         * Clear state of the widget.
         *
         * @returns {Widget}
         */
        self.clearState = function () {
            self.em.removeClass('has-success');
            self.em.removeClass('has-warning');
            self.em.removeClass('has-error');

            return self;
        };

        /**
         * Set state of the widget.
         *
         * @param type
         * @returns {Widget}
         */
        self.setState = function (type) {
            self.clearState();
            self.em.addClass('has-' + type);

            return self;
        };

        /**
         * Clear messages of the widget.
         *
         * @returns {Widget}
         */
        self.clearMessages = function () {
            if (self.messagesEm.length)
                self.messagesEm.html('');

            return self;
        };

        /**
         * Add a message to the widget
         *
         * @param msg
         * @returns {Widget}
         */
        self.addMessage = function (msg) {
            if (self.messagesEm.length)
                self.messagesEm.append('<span class="help-block">' + msg + '</span>');

            return self;
        };

        /**
         * Hide the widget.
         *
         * @returns {Widget}
         */
        self.hide = function () {
            self.em.addClass('hidden');

            return self;
        };

        /**
         * Show the widget.
         *
         * @returns {Widget}
         */
        self.show = function () {
            if (!self.alwaysHidden)
                self.em.removeClass('hidden');

            return self;
        };

        /*
         * Add a child widget.
         *
         * @returns {Widget}
         */
        self.addChild = function (child) {
            if (self.children.hasOwnProperty(child.uid))
                throw 'Widget ' + self.uid + ' already has child widget ' + child.uid;

            self.children[child.uid] = child;

            return self
        };

        // Load widget's assets
        if (self.jsModule.length) {
            require([self.jsModule], function (initCallback) {
                if ($.isFunction(initCallback)) {
                    initCallback(self);
                }
                else {
                    console.warn(self.jsModule + ' does not return a proper callback');
                }
            });
        }

        // Mark widget as initialized
        self.em.addClass('initialized');
        $(self).trigger('ready', [self]);

        // Create children widgets
        self.em.find(".pytsite-widget[data-parent-uid='" + self.uid + "']:not(.initialized)").each(function () {
            self.addChild(new Widget(this));
        });
    }

    /**
     * Initialize all non-initialized widgets found in the DOM
     */
    function initAll() {
        $('.pytsite-widget').not('.initialized').each(function () {
            new Widget(this);
        });
    }

    return {
        Widget: Widget,
        initAll: initAll
    }
});
