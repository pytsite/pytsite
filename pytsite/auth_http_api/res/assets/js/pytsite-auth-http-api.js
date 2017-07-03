define(['pytsite-http-api'], function (httpApi) {
    function isAnonymous() {
        return httpApi.get('auth/is_anonymous');
    }

    return {
        isAnonymous: isAnonymous
    }
});
