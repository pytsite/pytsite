define(['pytsite-http-api'], function (httpApi) {
    function isAnonymous() {
        return httpApi.get('auth/is_anonymous', null, 2);
    }

    return {
        isAnonymous: isAnonymous
    }
});
