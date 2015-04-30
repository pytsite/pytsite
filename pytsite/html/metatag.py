__tags = dict()

__allowed_tags = {
    'title',
    'author',
    'description'
}


def add(tag: str, value: str):
    if tag not in __allowed_tags:
        raise Exception('Unknown tag ' + tag)

    __tags[tag] = value
    pass


def add_multiple(tags: dict):
    """ Adds multiple tags
    :param tags:
    :return:
    """
    pass


def dump_tag(tag: str)->str:
    """ Dumps single tag
    :param tag:
    :return:
    """
    if tag not in __tags:
        raise Exception("Tag '{$tag}' is not registered")

    return tag + '->' + __tags[tag]


def dump_all()->str:
    r = str()
    for tag in __tags:
        r += dump_tag(tag)

    return r
