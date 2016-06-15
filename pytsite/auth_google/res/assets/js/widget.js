var pytsiteAuthDriverGoogleWidgetCount = 0;

/**
 * While writing code for this widget, refer to https://developers.google.com/identity/sign-in/web/reference
 */
$(window).on('pytsite.widget.init:pytsite.auth_google._driver._SignInWidget', function (e, widget) {
    function initButton(w) {
        var googleUserLoadCount = 0;
        var auth2 = gapi.auth2.getAuthInstance();

        // Wait while Google library detects current user
        auth2.currentUser.listen(function (user) {
            if (++googleUserLoadCount == 1) {
                // If user is signed out on PytSite, but signed in in Google, sign out it from Google
                pytsite.auth.isAnonymous().done(function (r) {
                    r && auth2.signOut();
                });
            }
            else {
                // Send given user for authentication to PytSite
                if (user.isSignedIn()) {
                    var form = w.em.closest('form');
                    var idToken = user.getAuthResponse().id_token;

                    form.find('input[id$="id-token"]').first().val(idToken);
                    form.submit();
                }
            }
        });

        // Render Google Sign In button
        gapi.signin2.render(w.uid);
    }

    $(window).on('pytsite.google.platform.ready', function () {
        // In case of multiple widgets on the page we need NOT to initialize it simultaneously,
        // so we init them with one-second timeout
        setTimeout(function () {
            if (!('auth2' in gapi)) {
                gapi.load('auth2', function () {
                    gapi.auth2.init({
                        client_id: widget.em.data('clientId')
                    });
                    initButton(widget);
                });
            }
            else {
                initButton(widget);
            }
        }, pytsiteAuthDriverGoogleWidgetCount++ * 1000);
    });
});
