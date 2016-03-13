pytsite.lang = {
    // Available languages, will be overwritten later by translations.js
    langs: [],

    // Translations, will be overwritten later by translations.js
    translations: {},

    current: function () {
        return document.documentElement.getAttribute('lang');
    },

    fallback: function () {
        return this.langs[0];
    },

    t: function (msg_id, args, language) {
        // Set current language
        if (typeof language == 'undefined')
            language = this.current();

        // Search for language
        if (this.langs.indexOf(language) < 0) {
            if (this.langs.length && language != this.fallback())
                return this.t(msg_id, args, this.fallback());
            else
                return msg_id;
        }

        var pkg = 'app'; // Default package
        var msg_parts = msg_id.split('@');

        // Split message ID into package name and message ID
        if (msg_parts.length == 2) {
            pkg = msg_parts[0];
            msg_id = msg_parts[1];
        }

        // Search for package
        if (!(pkg in this.translations[language])) {
            if (this.langs.length && language != this.fallback())
                return this.t(pkg + '@' + msg_id, args, this.fallback());
            else
                return pkg + '@' + msg_id;
        }

        // Search for message ID
        var pkg_strings = this.translations[language][pkg];
        if(!(msg_id in pkg_strings)) {
            if (this.langs.length && language != this.fallback())
                return this.t(pkg + '@' + msg_id, args, this.fallback());
            else
                return pkg + '@' + msg_id;
        }

        // Processing placeholders
        var translation = pkg_strings[msg_id];
        for (k in args)
            translation = translation.replace(':' + k, args[k])

        return translation;
    }
};

// Convenience shortcut
var t = function (msg_id, args, language) {
    return pytsite.lang.t(msg_id, args, language);
};
