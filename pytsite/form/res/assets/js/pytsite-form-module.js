define(['jquery', 'jquery-scroll-to', 'assetman', 'pytsite-http-api', 'pytsite-widget'], function ($, scrollTo, assetman, httpApi, widget) {
    var forms = {};

    var htmlEntityMap = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#39;',
        '/': '&#x2F;',
        '`': '&#x60;',
        '=': '&#x3D;'
    };

    function escapeHtml(s) {
        return String(s).replace(/[&<>"'`=\/]/g, function (s) {
            return htmlEntityMap[s];
        });
    }

    function getForm(id) {
        if (id in forms)
            return forms[id];
        else
            throw "Form '" + id + "' is not found";
    }

    function Form(em) {
        var self = this;
        self.em = em;
        self.id = em.attr('id');
        self.cid = em.data('cid');
        self.weight = parseInt(em.data('weight'));
        self.getWidgetsEp = em.data('getWidgetsEp');
        self.validationEp = em.data('validationEp');
        self.preventSubmit = em.data('preventSubmit') === 'True';
        self.isModal = em.data('modal') === 'True';
        self.modalEm = null;
        self.nocache = em.data('nocache') === 'True';
        self.submitEp = em.attr('submitEp');
        self.totalSteps = em.data('steps');
        self.currentStep = 0;
        self.isCurrentStepValidated = true;
        self.readyToSubmit = false;
        self.areas = {};
        self.title = self.em.find('.form-title');
        self.messages = self.em.find('.form-messages').first();
        self.widgets = {};

        if (self.isModal)
            self.modalEm = em.closest('.modal');

        // Initialize areas
        em.find('.form-area').each(function () {
            self.areas[$(this).data('formArea')] = $(this);
        });

        // Notify about form creation
        self.em.trigger('formReady', [self]);

        // Form submit handler
        self.em.submit(function (event) {
            // Form isn;t ready to submit, just move one step forward.
            if (!self.readyToSubmit) {
                event.preventDefault();
                self.forward();
            }
            // Form is ready to submit
            else {
                // Notify listeners about upcoming form submit
                self.em.trigger('formSubmit', [self]);

                if (self.preventSubmit) {
                    // Do nothing
                    event.preventDefault();
                }
                else {
                    // Remove all elements which should not be transfered to server
                    self.em.find('[data-skip-serialization=True]').remove();

                    // Add form data attributes as input elements
                    var formData = self.em.data();
                    for (var k in formData) {
                        if (formData.hasOwnProperty(k)) {
                            self.areas['hidden'].append($('<input name="__form_data_' + k + '" value="' + formData[k] + '">'));
                        }
                    }

                    // Disable submit button to prevent clicking it more than once while waiting for server response
                    self.em.find('.form-action-submit button').attr('disabled', true);
                }
            }
        });

        self.serialize = function (skipTags) {
            function getEmValue(em) {
                if (em.tagName === 'INPUT' && em.type === 'checkbox') {
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

                if ($(this).attr('data-skip-serialization') === 'True')
                    return;

                var dictListMatch = this.name.match(/([^\[]+)\[(\w+)\]\[\]$/);
                var listMatch = this.name.match(/\[\]$/);

                var fName = this.name;
                if (dictListMatch)
                    fName = dictListMatch[1];

                if (!(fName in r)) {
                    if (dictListMatch) {
                        r[fName] = {};
                        r[fName][dictListMatch[2]] = [getEmValue(this)];
                    }
                    else if (listMatch)
                        r[fName] = [getEmValue(this)];
                    else
                        r[fName] = getEmValue(this);
                }
                else {
                    if (dictListMatch) {
                        if (!(dictListMatch[2] in r[fName]))
                            r[fName][dictListMatch[2]] = [];
                        r[fName][dictListMatch[2]].push(getEmValue(this));
                    }
                    else if (listMatch)
                        r[fName].push(getEmValue(this));
                    else
                        r[fName] = getEmValue(this);
                }
            });

            for (var k in r) {
                if (r[k] instanceof Array && r[k].length === 1)
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
                if (emDataAttrs.hasOwnProperty(k)) {
                    data['__form_data_' + k] = emDataAttrs[k];
                }
            }

            // Merge data from location query
            $.extend(data, assetman.parseLocation(true).query);

            // Calculate form location string
            var q = assetman.parseLocation().query;
            $.extend(q, self.serialize(['TEXTAREA']));
            q['__form_data_step'] = self.currentStep;
            var formLocation = location.origin + location.pathname + '?' + assetman.encodeQuery(q);

            data['__form_data_step'] = self.currentStep;
            data['__form_data_location'] = formLocation;
            data['__form_data_uid'] = self.id;

            return httpApi.request(method, ep, data).fail(function (resp) {
                if ('responseJSON' in resp && 'error' in resp.responseJSON)
                    self.addMessage(resp.responseJSON.error, 'danger');
                else
                    self.addMessage(resp.statusText, 'danger');
            });
        };

        // Count widgets for the step
        self.countWidgets = function (step) {
            var r = 0;

            for (var uid in self.widgets) {
                if (self.widgets.hasOwnProperty(uid) && self.widgets[uid].formStep === step)
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

            msg = escapeHtml(msg);

            self.messages.append('<div class="alert alert-' + type + '" role="alert">' + msg + '</div>')
        };

        // Create widget from the raw data
        self.createWidget = function (widgetData) {
            // Create widget object
            var w = new widget.Widget(widgetData);

            // Widget replaces another one with different UID
            if (w.replaces === w.uid)
                self.removeWidget(w.uid);

            // Widget replaces another one with same UID
            if (w.uid in self.widgets)
                self.removeWidget(w.uid);

            // Append widget to the list of loaded widgets
            w.hide();
            self.widgets[w.uid] = w;

            return w;
        };

        // Place widget to the form
        self.addWidget = function (w) {
            if (w.parentUid) {
                if (w.parentUid in self.widgets)
                    self.widgets[w.parentUid].em.append(w.em);
                else
                    throw "Parent widget '{}' is not found".format(w.parentUid)
            }
            else {
                self.areas[w.formArea].append(w.em);
            }
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
        self.loadWidgets = function () {
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

            self._request('POST', self.getWidgetsEp + '/' + self.id).done(function (resp) {
                var numWidgetsToInit = resp.length;
                var progressCount = 1;

                for (var i = 0; i < numWidgetsToInit; i++) {
                    // Create widget from raw HTML data
                    var w = self.createWidget(resp[i]);
                    w.formStep = self.currentStep;

                    // Increase progress bar value
                    var percents = (100 / numWidgetsToInit) * progressCount++;
                    progressBar.width(percents + '%');
                    progressBar.attr('aria-valuenow', percents);

                    // This widget is the last one
                    if (self.countWidgets(self.currentStep) === numWidgetsToInit) {
                        // Sort all loaded widgets by weight
                        var sortedWidgets = [];
                        for (var uid in self.widgets) {
                            sortedWidgets.push(self.widgets[uid]);
                        }
                        sortedWidgets.sort(function (a, b) {
                            return a.weight - b.weight
                        });

                        // Add loaded widgets to the form
                        for (var k = 0; k < sortedWidgets.length; k++) {
                            self.addWidget(sortedWidgets[k]);
                        }

                        // Hide progress bar
                        clearInterval(progressBarInt);
                        progress.addClass('hidden');

                        // Fill widgets with data from location string
                        self.fill(assetman.parseLocation().query);

                        deffer.resolve();
                    }
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

                self._request('POST', self.validationEp + '/' + self.id).done(function (resp) {
                    if (resp.status) {
                        deffer.resolve();
                    }
                    else {
                        // Add error messages for widgets
                        for (var widget_uid in resp.messages) {
                            var w, widget_message;
                            if (widget_uid in self.widgets)
                                w = self.widgets[widget_uid];

                            // Convert single message to array for convenience
                            if (typeof resp.messages[widget_uid] === 'string') {
                                resp.messages[widget_uid] = [resp.messages[widget_uid]];
                            }

                            // Iterate over multiple messages for the same widget
                            for (var i = 0; i < resp.messages[widget_uid].length; i++) {
                                widget_message = resp.messages[widget_uid][i];

                                // If widget exists
                                if (w) {
                                    if (!w.alwaysHidden) {
                                        w.setState('error');
                                        w.addMessage(widget_message);
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
                }).fail(function () {
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
            for (var uid in self.widgets) {
                if (self.widgets[uid].formStep === step)
                    self.widgets[uid].show();
            }

            return self;
        };

        // Hide widgets for the step
        self.hideWidgets = function (step) {
            for (var uid in self.widgets) {
                if (self.widgets[uid].formStep === step)
                    self.widgets[uid].hide();
            }

            return self;
        };

        // Remove widgets for the step
        self.removeWidgets = function (step) {
            for (var uid in self.widgets) {
                if (self.widgets[uid].formStep === step)
                    self.removeWidget(uid);
            }
        };

        // Move to the next step
        self.forward = function () {
            var deffer = $.Deferred();
            var submitButton = self.em.find('.form-action-submit button');

            // Validating the form for the current step
            submitButton.attr('disabled', true);
            self.validate().done(function () {
                // Disable user activity while widgets are loading
                submitButton.attr('disabled', false);

                // It is not a last step, so just load and show widgets for the next step
                if (self.currentStep < self.totalSteps) {
                    // Hide widgets for the current step
                    self.hideWidgets(self.currentStep);

                    // Step change
                    ++self.currentStep;

                    // Load widgets for the current step
                    self.loadWidgets().done(function () {
                        // Attach click handler to the 'Backward' button
                        self.em.find('.form-action-backward').click(self.backward);

                        // Mark current step as is not validated
                        self.isCurrentStepValidated = false;

                        // Show widgets
                        self.showWidgets(self.currentStep);

                        // Notify listeners
                        $(self.em).trigger('formForward', [self]);
                        deffer.resolve();

                        // Scroll to top of the page
                        if (self.currentStep > 1) {
                            $.scrollTo(self.em, 250);
                        }
                    });
                }
                // It is a last step, just allowing submit the form
                else {
                    self.readyToSubmit = true;
                    self.em.submit();
                }
            }).fail(function () {
                submitButton.attr('disabled', false);
                deffer.reject();
            });

            return deffer;
        };

        // Move to the previous step
        self.backward = function () {
            self.removeWidgets(self.currentStep);
            self.showWidgets(--self.currentStep);
            $.scrollTo(self.em, 250);
        };

        /**
         * Reset form's HTML element
         */
        self.reset = function () {
            self.em[0].reset();
        }
    }

    return {
        Form: Form
    }
});
