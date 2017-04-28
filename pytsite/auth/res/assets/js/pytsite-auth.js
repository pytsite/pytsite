define(['pytsite-http-api'], function (httpApi) {
    function getLoginForm(driver, title, uid, css, modal, success) {
        httpApi.get('auth/login_form', {
            driver: driver,
            title: title,
            uid: uid,
            css: css,
            modal: modal
        }).done(function (resp) {
            if (success)
                success(resp);
        });
    }

    function isAnonymous() {
        return httpApi.get('auth/is_anonymous');
    }

    return {
        getLoginForm: getLoginForm,
        isAnonymous: isAnonymous
    }
});
