define(['pytsite-lang-translations'], function(translations) {
    function current() {
        return document.documentElement.getAttribute('lang');
    }

    function fallback() {
        return langs[0];
    }

    function t(msg_id, args, language) {
        if (typeof language === 'undefined')
            language = current();

        // Search for language
        if (translations.langs.indexOf(language) < 0) {
            if (translations.langs.length && language !== fallback())
                return t(msg_id, args, fallback());
            else
                return msg_id;
        }

        var pkg = 'app'; // Default package
        var msg_parts = msg_id.split('@');

        // Split message ID into package name and message ID
        if (msg_parts.length === 2) {
            pkg = msg_parts[0];
            msg_id = msg_parts[1];
        }

        // Search for package
        if (!(pkg in translations.translations[language])) {
            if (translations.langs.length && language !== fallback())
                return t(pkg + '@' + msg_id, args, fallback());
            else
                return pkg + '@' + msg_id;
        }

        // Search for message ID
        var pkg_strings = translations.translations[language][pkg];
        if(!(msg_id in pkg_strings)) {
            if (translations.langs.length && language !== fallback())
                return t(pkg + '@' + msg_id, args, fallback());
            else
                return pkg + '@' + msg_id;
        }

        // Processing placeholders
        var translation = pkg_strings[msg_id];
        for (var k in args) {
            if (args.hasOwnProperty(k))
                translation = translation.replace(':' + k, args.k);
        }

        return translation;
    }

    return {
        current: current,
        fallback: fallback,
        t: t
    }
});
