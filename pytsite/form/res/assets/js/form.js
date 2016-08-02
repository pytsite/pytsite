pytsite.form = {
    forms: {},

    getForm: function (id) {
        if (id in pytsite.form.forms)
            return pytsite.form.forms[id];
        else
            throw "Form '" + id + "' is not found";
    },

    Form: function (em) {
        var self = this;
        self.em = em;
        self.id = em.attr('id');
        self.cid = em.data('cid');
        self.weight = parseInt(em.data('weight'));
        self.getWidgetsEp = em.data('getWidgetsEp');
        self.validationEp = em.data('validationEp');
        self.reloadOnForward = em.data('reloadOnForward') == 'True';
        self.preventSubmit = em.data('preventSubmit') == 'True';
        self.isModal = em.data('modal') == 'True';
        self.submitEp = em.attr('submitEp');
        self.totalSteps = em.data('steps');
        self.loadedSteps = [];
        self.currentStep = 0;
        self.isCurrentStepValidated = true;
        self.readyToSubmit = false;
        self.areas = {};
        self.title = self.em.find('.form-title');
        self.messages = self.em.find('.form-messages').first();
        self.widgets = {};

        // Initialize areas
        em.find('.form-area').each(function () {
            self.areas[$(this).data('formArea')] = $(this);
        });

        // Form submit handler
        self.em.submit(function (event) {
            // If form has more than 1 step and it is not last step.
            // Just move one step forward.
            if (!self.readyToSubmit) {
                event.preventDefault();
                self.forward();
            }
            else {
                $(window).trigger('pytsite.form.submit', [self]);

                if (self.preventSubmit)
                    event.preventDefault();
                else
                    self.em.find('.form-action-submit button').attr('disabled', true);
            }
        });

        self.serialize = function (skipTags) {
            function getEmValue(em) {
                if (em.tagName == 'INPUT' && em.type == 'checkbox') {
                    if (em.name.indexOf('[]') > 0)
                        return em.value;
                    else
                        return em.checked;
                }
                else
                    return em.value;
            }

            var r = {};

            self.em.find('[name]').each(function () {
                if (skipTags instanceof Array && this.tagName in skipTags)
                    return;

                if (!(this.name in r)) {
                    if (this.name.indexOf('[]') > 0)
                        r[this.name] = [getEmValue(this)];
                    else
                        r[this.name] = getEmValue(this);
                }
                else {
                    if (r[this.name] instanceof Array)
                        r[this.name].push(getEmValue(this));
                    else
                        r[this.name] = getEmValue(this);
                }
            });

            for (var k in r) {
                if (r[k] instanceof Array && r[k].length == 1)
                    r[k] = r[k][0];
            }

            return r;
        };

        // Do an AJAX request
        self._request = function (method, ep) {
            var data = self.serialize();

            // Add form's data-attributes
            var emDataAttrs = self.em.data();
            for (var k in emDataAttrs) {
                if ($.inArray(k, ['getWidgetsEp', 'validationEp', 'reloadOnForward', 'steps']) < 0)
                    data['__form_data_' + k] = emDataAttrs[k];
            }

            // Merge data from location query
            $.extend(data, pytsite.browser.parseLocation(true).query);

            // Calculate form location string
            var q = pytsite.browser.parseLocation().query;
            $.extend(q, self.serialize(['TEXTAREA']));
            q['__form_data_step'] = self.currentStep;
            var formLocation = location.origin + location.pathname + '?' + pytsite.browser.encodeQuery(q);

            data['__form_data_step'] = self.currentStep;
            data['__form_data_location'] = formLocation;

            return pytsite.httpApi.request(method, ep, data)
                .fail(function (resp) {
                    if ('responseJSON' in resp && 'error' in resp.responseJSON)
                        self.addMessage(resp.responseJSON.error, 'danger');
                    else
                        self.addMessage(resp.statusText, 'danger');
                });
        };

        // Count widgets for current step
        self.count = function () {
            var r = 0;
            for (var uid in self.widgets) {
                if (self.widgets[uid].formStep == self.currentStep)
                    ++r;
            }

            return r;
        };

        // Set form's title
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
        self.loadWidget = function (widgetData, index) {
            var deffer = $.Deferred();

            // Initialize widget
            var widget = new pytsite.widget.Widget(widgetData);

            $(widget)
                .on('ready', function () {
                    if (widget.uid in self.widgets) {
                        if (widget.replaces == widget.uid)
                            self.removeWidget(widget.uid);
                        else
                            throw "Widget '" + widget.uid + "' already exists.";
                    }

                    // Append widget to the form
                    widget.hide();
                    self.widgets[widget.uid] = widget;

                    $(self).trigger('widgetReady', [widget]);

                    deffer.resolve(index);
                })
                .on('initError', function () {
                    deffer.reject(index);
                });

            return deffer;
        };

        // Get widget of the form
        self.getWidget = function (uid) {
            if (!(uid in self.widgets))
                throw "Widget '" + uid + "' does not exist.";

            return self.widgets[uid];
        };

        // Remove widget from the form
        self.removeWidget = function (uid) {
            if (!(uid in self.widgets))
                return;

            self.widgets[uid].em.remove();
            delete self.widgets[uid];
        };

        // Load widgets for the current step
        self.loadWidgets = function (showAfterLoad) {
            var deffer = $.Deferred();
            var progress = self.areas['body'].find('.progress');
            var progressBar = progress.find('.progress-bar');

            // Show progress bar
            progress.removeClass('hidden');
            progressBar.css('width', '0');

            // Progress bar smooth update
            var progressBarInt = setInterval(function () {
                var percents = parseInt(progressBar.attr('aria-valuenow')) + 1;
                if (percents <= 100) {
                    progressBar.width(percents + '%');
                    progressBar.attr('aria-valuenow', percents);
                }
            }, 250);

            self._request('POST', self.getWidgetsEp)
                .done(function (resp) {
                    var numWidgetsToLoad = resp.length;
                    var progressCount = 1;

                    for (var i = 0; i < numWidgetsToLoad; i++) {
                        // Append widget
                        self.loadWidget(resp[i], i)
                            .done(function (index) {
                                // Increase progress bar value
                                var percents = (100 / numWidgetsToLoad) * progressCount++;
                                progressBar.width(percents + '%');
                                progressBar.attr('aria-valuenow', percents);

                                // This widget is the last one
                                if (self.count() == numWidgetsToLoad) {
                                    // Sort all loaded widgets by weight
                                    var sortedWidgets = [];
                                    for (var uid in self.widgets) {
                                        sortedWidgets.push(self.widgets[uid]);
                                    }
                                    sortedWidgets.sort(function (a, b) {
                                        return a.weight - b.weight
                                    });

                                    // Place loaded widgets to the form
                                    for (var k = 0; k < sortedWidgets.length; k++) {
                                        var formArea = sortedWidgets[k].formArea;
                                        var widget = sortedWidgets[k];

                                        if (widget.parentUid) {
                                            if (widget.parentUid in self.widgets)
                                                self.widgets[widget.parentUid].em.append(widget.em);
                                            else
                                                throw "Parent widget '{0}' is not found".format(widget.parentUid)
                                        }
                                        else
                                            self.areas[formArea].append(widget.em);
                                    }

                                    // Hide progress bar
                                    clearInterval(progressBarInt);
                                    progress.addClass('hidden');

                                    // Fill widgets with data from location string
                                    self.fill(pytsite.browser.parseLocation().query);

                                    // Show loaded widgets
                                    if (showAfterLoad == true)
                                        self.showWidgets();

                                    deffer.resolve();
                                }
                            });
                    }
                });

            return deffer;
        };

        // Fill form with data
        self.fill = function (data) {
            for (k in data)
                self.em.find('[name="' + k + '"]').val(data[k]);

            return self;
        };

        // Do form validation
        self.validate = function () {
            var deffer = $.Deferred();

            // Mark current step as validation when validation will finish
            deffer.done(function () {
                self.isCurrentStepValidated = true;
            });

            if (self.currentStep > 0) {
                // Reset form's messages
                self.clearMessages();

                // Reset widgets state
                for (var uid in self.widgets)
                    self.widgets[uid].clearState().clearMessages();

                self._request('POST', self.validationEp)
                    .done(function (resp) {
                        if (resp.status) {
                            deffer.resolve();
                        }
                        else {
                            // Add error messages for widgets
                            for (var widget_uid in resp.messages) {
                                var widget, widget_message;
                                if (widget_uid in self.widgets)
                                    widget = self.widgets[widget_uid];

                                // Convert single message to array for convenience
                                if (typeof resp.messages[widget_uid] == 'string') {
                                    resp.messages[widget_uid] = [resp.messages[widget_uid]];
                                }

                                // Iterate over multiple messages for the same widget
                                for (var i = 0; i < resp.messages[widget_uid].length; i++) {
                                    widget_message = resp.messages[widget_uid][i];

                                    // If widget exists
                                    if (widget) {
                                        if (!widget.alwaysHidden) {
                                            widget.setState('error');
                                            widget.addMessage(widget_message);
                                        }
                                        else {
                                            self.addMessage(widget_uid + ': ' + widget_message, 'danger');
                                        }
                                    }
                                    // Widget does not exist
                                    else {
                                        self.addMessage(widget_uid + ': ' + widget_message, 'danger');
                                    }
                                }
                            }

                            var scrollObject = $(window);
                            if (self.isModal)
                                scrollObject = self.em.closest('.modal');

                            var scrollToTarget = self.em.find('.has-error').first();
                            if (!scrollToTarget.length)
                                scrollToTarget = self.messages;

                            scrollObject.scrollTo(scrollToTarget, 250);
                            deffer.reject();
                        }
                    })
                    .fail(function () {
                        $(window).scrollTo(0, 250);
                        deffer.reject();
                    });
            }
            else {
                deffer.resolve();
            }

            return deffer;
        };

        // Show widgets for the step
        self.showWidgets = function (step) {
            if (step == undefined)
                step = self.currentStep;

            for (var uid in self.widgets) {
                if (self.widgets[uid].formStep == step)
                    self.widgets[uid].show();
            }

            return self;
        };

        // Hide widgets for the step
        self.hideWidgets = function (step) {
            if (step == undefined)
                step = self.currentStep;

            for (var uid in self.widgets) {
                if (self.widgets[uid].formStep == step)
                    self.widgets[uid].hide();
            }

            return self;
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
            var deffer = $.Deferred();
            var submitButton = self.em.find('.form-action-submit button');

            // Validating the form for the current step
            submitButton.attr('disabled', true);
            self.validate()
                .done(function () {
                    submitButton.attr('disabled', false);

                    // It is not a last step, so just load (if necessary) and show widgets for the next step
                    if (self.currentStep < self.totalSteps) {
                        // Hide widgets for the current step
                        self.hideWidgets();

                        // Step change
                        ++self.currentStep;

                        // Load widgets via AJAX request, if necessary
                        if ($.inArray(self.currentStep, self.loadedSteps) < 0 || self.reloadOnForward) {
                            // First, remove all existing widgets for the current step
                            self.removeWidgets(self.currentStep);

                            // Load widgets for the current step
                            self.loadWidgets()
                                .done(function () {
                                    if ($.inArray(self.currentStep, self.loadedSteps) < 0)
                                        self.loadedSteps.push(self.currentStep);

                                    // Attach click handler to the 'Backward' button
                                    self.em.find('.form-action-backward').click(self.backward);

                                    // Show widgets
                                    self.isCurrentStepValidated = false;
                                    self.showWidgets();
                                    $(self).trigger('pytsite.form.forward');
                                    deffer.resolve();
                                });
                        }
                        // Just show widgets, if they already loaded
                        else {
                            // Show widgets
                            self.isCurrentStepValidated = false;
                            self.showWidgets();
                            $(self).trigger('pytsite.form.forward');
                            deffer.resolve();
                        }
                    }
                    // It is a last step, just allowing submit the form
                    else {
                        self.readyToSubmit = true;
                        self.em.submit();
                    }
                })
                .fail(function () {
                    submitButton.attr('disabled', false);
                    deffer.reject();
                });

            return deffer;
        };

        // Move to the previous step
        self.backward = function () {
            self.hideWidgets(self.currentStep);
            --self.currentStep;
            self.showWidgets(self.currentStep)
        };
    }
};


$(function () {
    // Initialize all forms on the page after page loading
    $('.pytsite-form').each(function () {
        // Create form
        var form = new pytsite.form.Form($(this));

        // Add form to forms collection
        pytsite.form.forms[form.id] = form;

        // Notify about form creation
        $(window).trigger('pytsite.form.ready', [form]);

        // If requested to walk to particular step automatically
        var q = pytsite.browser.parseLocation().query;
        var walkToStep = '__form_data_step' in q ? parseInt(q['__form_data_step']) : 1;
        $(form).on('pytsite.form.forward', function () {
            // When form will make its first step, move it automatically to the requested step
            if (form.currentStep < walkToStep)
                form.forward();
        });

        // Do the first step
        form.forward();
    });
});
