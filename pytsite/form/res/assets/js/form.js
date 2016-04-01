$.fn.serializeForm = function () {
    var o = {};
    var a = this.serializeArray();

    $.each(a, function () {
        if (o[this.name] !== undefined) {
            if (!o[this.name].push)
                o[this.name] = [o[this.name]];

            o[this.name].push(this.value || '');
        }
        else
            o[this.name] = this.value || '';
    });

    return o;
};

pytsite.form = {
    Widget: function (uid, content, formArea, formStep, weight, assets) {
        var self = this;
        self.uid = uid;
        self.formArea = formArea;
        self.formStep = formStep;
        self.weight = weight;
        self.assets = assets;
        self.content = $(content);
        self.em = $('<div class="pytsite-form-widget-wrapper hidden">');
        self.messagesEm = $('<div class="messages">');

        // Append widget's HTML to the container
        self.em.append(self.content);

        // Additional styles depends on widget's HTML tag
        if ($.inArray(self.content.prop('tagName'), ['A', 'BUTTON', 'SPAN']) >= 0)
            self.em.addClass('inline');

        // Add block for messages
        var fGroup = self.em.find('.form-group');
        if (fGroup.length)
            fGroup.append(self.messagesEm);
        else
            self.em.append(self.messagesEm);

        // Load widget's assets
        pytsite.browser.addAssets(self.assets);

        // Initialize widget
        $(window).trigger('pytsite.widget.init', self);

        self.resetState = function () {
            self.em.removeClass('has-success');
            self.em.removeClass('has-warning');
            self.em.removeClass('has-error');

            return self;
        };

        self.setState = function (type) {
            self.resetState();
            self.em.addClass('has-' + type);

            return self;
        };

        self.clearMessages = function () {
            self.messagesEm.html('');

            return self;
        };

        self.addMessage = function (msg) {
            self.messagesEm.append('<span class="help-block">{0}</span>'.format(msg));

            return self;
        };

        self.hide = function () {
            self.em.addClass('hidden');

            return self;
        };

        self.show = function () {
            self.em.removeClass('hidden');

            return self;
        };
    },

    Form: function (em) {
        var self = this;
        self.em = em;
        self.id = em.attr('id');
        self.cid = em.data('cid');
        self.getWidgetsEp = em.data('getWidgetsEp');
        self.validationEp = em.data('validationEp');
        self.reloadOnForward = em.data('reloadOnForward') == 'True';
        self.submitEp = em.attr('submitEp');
        self.totalSteps = em.data('steps');
        self.loadedSteps = [];
        self.currentStep = 0;
        self.readyToSubmit = false;
        self.areas = {};
        self.title = self.em.find('.form-title');
        self.messages = self.em.find('.form-messages');
        self.widgets = {};

        em.find('.form-area').each(function () {
            self.areas[$(this).data('formArea')] = $(this);
        });

        self.serialize = function () {
            var r = {};

            $.each(self.em.serializeArray(), function () {
                if (r[this.name] !== undefined) {
                    if (!r[this.name].push)
                        r[this.name] = [r[this.name]];

                    r[this.name].push(this.value || '');
                }
                else
                    r[this.name] = this.value || '';
            });

            return r;
        };

        // Do an AJAX request
        self._request = function (method, ep) {
            var emDataAttrs = self.em.data();
            var data = {};
            for (k in emDataAttrs)
                data['__form_data_' + k] = emDataAttrs[k];

            $.extend(data, self.serialize());

            return pytsite.ajax.request(method, ep, data)
                .fail(function (resp) {
                    if ('responseJSON' in resp && 'error' in resp.responseJSON)
                        self.addMessage(resp.responseJSON.error, 'danger');
                    else
                        self.addMessage(resp.statusText, 'danger');
                });
        };

        // Get form's title
        self.setTitle = function (title) {
            self.title.html('<h4>' + title + '</h4>');
        };

        // Clear form's messages
        self.clearMessages = function () {
            self.messages.html('');
        };

        // Add a message to the form
        self.addMessage = function (msg, type) {
            if (!type)
                type = 'info';

            self.messages.append('<div class="alert alert-' + type + '" role="alert">' + msg + '</div>')
        };

        // Add a widget to the form
        self.addWidget = function (w) {
            if (w.uid in self.widgets)
                throw "Widget '{0}' already exists.".format(w.uid);

            var widget = new pytsite.form.Widget(w.uid, w.content, w.formArea, w.formStep, w.weight, w.assets);

            // Append widget's HTML to DOM
            self.areas[widget.formArea].append(widget.em);
            self.widgets[widget.uid] = widget;
        };

        // Remove widget from the form
        self.removeWidget = function (uid) {
            if (!(uid in self.widgets))
                return;

            self.widgets[uid].em.remove();
            delete self.widgets[uid];
        };

        // Load widgets for the current step
        self.loadWidgets = function () {
            return self._request('GET', self.getWidgetsEp)
                .done(function (resp) {
                    for (var i = 0; i < resp.length; i++)
                        self.addWidget(resp[i]);

                    self.areas['body'].find('.loading').remove();
                });
        };

        // Do form validation
        self.validate = function () {
            // Reset widgets state
            for (var uid in self.widgets)
                self.widgets[uid].resetState().clearMessages();

            var validateDeferred = $.Deferred();

            self._request('POST', self.validationEp).done(function (resp) {
                if (resp.status) {
                    validateDeferred.resolve();
                }
                else {
                    // Add error messages for widgets
                    for (var uid in resp.messages) {
                        if (uid in self.widgets) {
                            var widget = self.widgets[uid];
                            widget.setState('error');

                            for (var i = 0; i < resp.messages[uid].length; i++) {
                                widget.addMessage(resp.messages[uid]);
                            }
                        }
                    }

                    validateDeferred.reject();
                }
            });

            return validateDeferred;
        };

        // Show widgets for the step
        self.showWidgets = function (step) {
            for (var uid in self.widgets) {
                if (self.widgets[uid].formStep == step)
                    self.widgets[uid].show();
            }
        };

        // Hide widgets for the step
        self.hideWidgets = function (step) {
            for (var uid in self.widgets) {
                if (self.widgets[uid].formStep == step)
                    self.widgets[uid].hide();
            }
        };

        // Remove widgets for the step
        self.removeWidgets = function (step) {
            for (var uid in self.widgets) {
                if (self.widgets[uid].formStep == step)
                    self.removeWidget(uid);
            }
        };

        // Move to the next step
        self.forward = function () {
            self.hideWidgets(self.currentStep);
            ++self.currentStep;

            if ($.inArray(self.currentStep, self.loadedSteps) < 0 || self.reloadOnForward) {
                self.removeWidgets(self.currentStep);

                self.loadWidgets()
                    .done(function () {
                        if ($.inArray(self.currentStep, self.loadedSteps) < 0)
                            self.loadedSteps.push(self.currentStep);

                        // Attach click handler to the 'Backward' button
                        self.em.find('.form-action-backward').click(self.backward);

                        self.showWidgets(self.currentStep)
                    });
            }
            else
                self.showWidgets(self.currentStep);
        };

        // Move to the previous step
        self.backward = function () {
            self.hideWidgets(self.currentStep);
            --self.currentStep;
            self.showWidgets(self.currentStep)
        };

        // Submit event handler
        self.em.submit(function (event) {
            if (!self.readyToSubmit) {
                event.preventDefault();

                self.validate().done(function () {
                    if (self.currentStep < self.totalSteps)
                        self.forward();
                    else {
                        self.readyToSubmit = true;
                        self.em.submit();
                    }
                });
            }
        });
    }
};


$(function () {
    $('.pytsite-form').each(function () {
        var form = new pytsite.form.Form($(this));
        form.forward();
    });
});
