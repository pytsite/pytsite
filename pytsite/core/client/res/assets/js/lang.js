pytsite.lang = {
    t: function t(msg_id, args) {
        var pkg = 'app';
        var msg_parts = msg_id.split('@');

        if(msg_parts.length == 2) {
            pkg = msg_parts[0];
            msg_id = msg_parts[1];
        }

        var pkg_strings = pytsite.lang.translations[pytsite.lang.current_lang][pkg];
        if(pkg_strings === undefined)
            return pkg + '@' + msg_id;

        var translation = pkg_strings[msg_id];
        if(translation === undefined)
            return pkg + '@' + msg_id;

        for(k in args)
            translation = translation.replace(':' + k, args[k])

        return translation;
    },
    langs: [],
    current_lang: null,
    translations: {}
};

t = pytsite.lang.t;
