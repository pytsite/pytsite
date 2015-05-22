"""Admin Sidebar.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from pytsite.core.util import dict_sort
from pytsite.core.html import Aside, Section, Ul, Li, Span, A, I


__sections = {}


def add_section(uid: str, title: str, weight: int=0):
    """Add a section.
    """

    global __sections

    if uid in __sections:
        raise KeyError("Section '{}' already exists.".format(uid))

    __sections[uid] = {'title': title, 'weight': weight, 'menus': {}}


def add_section_menu(section_uid: str, menu_uid: str, title: str, href: str='#', icon: str=None,
                     label: str=None, label_class: str='primary', weight: int=0):
    """Add a menu to a section.
    """

    global __sections

    if section_uid not in __sections:
        raise KeyError("Section '{}' is not exists.".format(section_uid))

    section = __sections[section_uid]
    if menu_uid in section['menus']:
        raise KeyError("Menu '{}' already defined in section '{}'.".format(menu_uid, section_uid))

    section['menus'][menu_uid] = {
        'title': title,
        'href': href,
        'icon': icon,
        'label': label,
        'label_class': label_class,
        'weight': weight,
        'children': []
    }


def get_section_menu(section_uid: str, menu_uid: str) -> dict:
    """Get a menu of a section.
    """

    global __sections

    if section_uid not in __sections:
        raise KeyError("Section '{}' is not exists.".format(section_uid))

    section = __sections[section_uid]
    if menu_uid not in section['children']:
        raise KeyError("Menu '{}' is not defined in section '{}'.".format(menu_uid, section_uid))


def add_section_menu_child(section_uid: str, menu_uid: str, title: str, href: str, weight: 0):
    menu = get_section_menu(section_uid, menu_uid)
    menu['children'].append({'title': title, 'href': href, 'weight': weight})


def render() -> str:
    """Render the admin sidebar.
    """

    global __sections

    aside_em = Aside(cls='main-sidebar')
    sidebar_section_em = Section(cls='sidebar')
    aside_em.append(sidebar_section_em)

    root_menu_ul = Ul(cls='sidebar-menu')
    sidebar_section_em.append(root_menu_ul)

    for section_uid, section in dict_sort(__sections).items():
        root_menu_ul.append(Li(section['title'], cls='header'))
        for section_menu_uid, section_menu in dict_sort(section['menus']).items():
            if section_menu['children']:
                pass
            else:
                a = A(href=section_menu['href'])
                if section_menu['icon']:
                    a.append(I(cls=section_menu['icon']))
                a.append(Span(section_menu['title']))
                if section_menu['label']:
                    label_class = 'label pull-right label-' + section_menu['label_class']
                    a.append(Span(section_menu['label'], cls=label_class))

                root_menu_ul.append(Li().append(a))

    return aside_em.render()
