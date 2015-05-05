_languages = []
_current_language = None
_packages = {}


def define_languages(languages: list):
    """Define available languages.
    """
    global _languages
    _languages = languages
    set_lang(languages[0])


def get_languages():
    """Get all available languages.
    """
    return _languages


def set_lang(code: str):
    """Set current default language.
    """
    if code not in _languages:
        raise Exception("Language '{0}' is not defined.".format(code))


def get_lang()->str:
    """Get current default language.
    """
    if not _languages:
        raise Exception("No languages are defined.")

    global _current_language
    if not _current_language:
        _current_language = _languages[0]

    return _current_language


def register_package(package_name: str, languages_dir: str='lng')->str:
    """Register language container.
    """
    from importlib.util import find_spec
    spec = find_spec(package_name)
    if not spec:
        raise Exception("Package '{0}' is not found.".format(package_name))

    from os import path
    lng_dir = path.join(path.dirname(spec.origin), languages_dir)
    if not path.isdir(lng_dir):
        raise Exception("Directory '{0}' is not exists.".format(lng_dir))

    _packages[package_name] = {'_path': lng_dir}


def translate(msg_id: str, language: str=None)->str:
    """Translate a string.
    """
    if not language:
        language = get_lang()

    if language not in _languages:
        raise Exception("Language '{0}' is not defined.".format(language))

    # Determining package name and message ID
    package_name = 'app'
    msg_id = msg_id.split('@')
    if len(msg_id) == 2:
        package_name = msg_id[0]
        msg_id = msg_id[1]
    else:
        msg_id = msg_id[0]

    content = _load_file(package_name, language)
    if msg_id not in content:
        return package_name + '@' + msg_id

    return content[msg_id]


def transliterate(text: str)->str:
    """Transliterate a string.
    """
    cyrillic = [
        "Щ", "щ", 'Ё', 'Ж', 'Х', 'Ц', 'Ч', 'Ш', 'Ю', 'Я',
        'ё', 'ж', 'х', 'ц', 'ч', 'ш', 'ю', 'я', 'А', 'Б',
        'В', 'Г', 'Д', 'Е', 'З', 'И', 'Й', 'К', 'Л', 'М',
        'Н', 'О', 'П', 'Р', 'С', 'Т', 'У', 'Ф', 'Ь', 'Ы',
        'Ъ', 'Э', 'а', 'б', 'в', 'г', 'д', 'е', 'з', 'и',
        'і', 'й', 'к', 'л', 'м', 'н', 'о', 'п', 'р', 'с',
        'т', 'у', 'ф', 'ь', 'ы', 'ъ', 'э', 'Ї', 'ї', 'Є',
        'є', 'Ґ', 'ґ']

    roman = [
        "Sch", "sch", 'Yo', 'Zh', 'Kh', 'Ts', 'Ch', 'Sh', 'Yu', 'Ya',
        'yo', 'zh', 'kh', 'ts', 'ch', 'sh', 'yu', 'ya', 'A', 'B',
        'V', 'G', 'D', 'E', 'Z', 'I', 'Y', 'K', 'L', 'M',
        'N', 'O', 'P', 'R', 'S', 'T', 'U', 'F', '', 'Y',
        '', 'E', 'a', 'b', 'v', 'g', 'd', 'e', 'z', 'i',
        'i', 'y', 'k', 'l', 'm', 'n', 'o', 'p', 'r', 's',
        't', 'u', 'f', '', 'y', '', 'e', 'i', 'i', 'Ye',
        'ye', 'G', 'g'
    ]

    r = ''
    for ch in text:
        try:
            i = cyrillic.index(ch)
            r += roman[i]
        except ValueError:
            r += ch

    return r


def _load_file(package_name: str, language: str=None):
    """Load package's language file.
    """
    # Is package registered?
    if package_name not in _packages:
        raise Exception("Package '{0}' is not registered.".format(package_name))

    if not language:
        language = get_lang()

    # Getting from cache
    if language in _packages[package_name]:
        return _packages[package_name][language]

    # Actual data loading
    from os import path
    file_path = path.join(_packages[package_name]['_path'], language + '.yml')
    file = open(file_path)
    import yaml
    content = yaml.load(file)
    file.close()

    # Caching
    _packages[package_name][language] = content

    return content