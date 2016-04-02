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
            var data = {
                __form_data_step: self.currentStep
            };
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
        self.addWidget = function (widgetData) {
            // Initialize widget
            var widget = new pytsite.widget.Widget(widgetData);

            if (widget.uid in self.widgets)
                throw "Widget '" + widget.uid + "' already exists.";

            // Append widget to the form
            widget.hide();
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
                    var progress = self.areas['body'].find('.progress');
                    var totalWidgets = resp.length;

                    for (var i = 0; i < totalWidgets; i++) {
                        var percents = (100 / totalWidgets) * (i + 1);
                        progress.find('.progress-bar').css('width', percents + '%');

                        self.addWidget(resp[i]);
                    }

                    progress.addClass('hidden');
                });
        };

        // Do form validation
        self.validate = function () {
            // Reset widgets state
            for (var uid in self.widgets)
                self.widgets[uid].clearState().clearMessages();

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
