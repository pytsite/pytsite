define(['pytsite-http-api'], function (httpApi) {
    function getEntities(model, args) {
        return httpApi.get('odm/entities/' + model, args);
    }

    function getEntity(model, uid, args) {
        return httpApi.get('odm/entity/' + model + '/' + uid, args);
    }

    function postEntity(model, data) {
        return httpApi.post('odm/entity/' + model, data);
    }

    function patchEntity(model, uid, data) {
        return httpApi.patch('odm/entity/' + model + '/' + uid, data);
    }

    function deleteEntity(model, uid) {
        return httpApi.del('odm/entity/' + model + '/' + uid);
    }

    return {
        getEntities: getEntities,
        getEntity: getEntity,
        postEntity: postEntity,
        patchEntity: patchEntity,
        deleteEntity: deleteEntity
    }
});
