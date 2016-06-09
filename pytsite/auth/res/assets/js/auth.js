pytsite.auth = {
    getLoginForm: function (driver, title, uid, css, modal, success) {
        pytsite.jsApi.get('pytsite.auth.get_login_form', {
            driver: driver,
            title: title,
            uid: uid,
            css: css,
            modal: modal
        }, function (resp) {
            if (success)
                success(resp);
        });
    },

    isAnonymous: function () {
        return pytsite.jsApi.get('pytsite.auth@is_anonymous');
    }
};
