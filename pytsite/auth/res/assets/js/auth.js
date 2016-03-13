pytsite.auth = {
    getLoginForm: function(driver, title, uid, css, modal, success) {
        pytsite.ajax.get('pytsite.auth.ajax.get_login_form', {
            driver: driver,
            title: title,
            uid: uid,
            css: css,
            modal: modal
        }, function(resp) {
            if (success)
                success(resp);
        });
    },

    isAnonymous: function(yes, no) {
        pytsite.ajax.get('pytsite.auth.ajax.is_anonymous', {}, function(resp) {
            if(resp instanceof Boolean) {
                if (resp)
                    yes();
                else
                    no();
            }
        });
    }
};