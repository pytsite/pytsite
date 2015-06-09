"""Admin Sidebar.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from copy import deepcopy
from pytsite.core import router
from pytsite.core.util import weight_sort
from pytsite.core.html import Aside, Section, Ul, Li, Span, A, I
from pytsite.auth import auth_manager

__sections = []
__last_section_weight = 0


def get_section(sid: str) -> dict:
    """Get section.
    """
    for s in __sections:
        if s['sid'] == sid:
            return s


def add_section(sid: str, title: str, weight: int=0, permissions: tuple=()):
    """Add a section.
    """
    global __last_section_weight, __sections

    if get_section(sid):
        raise KeyError("Section '{}' already exists.".format(sid))

    if not weight:
        weight = __last_section_weight + 100

    __last_section_weight = weight
    __sections.append({
        'sid': sid,
        'title': title,
        'weight': weight,
        'children': [],
        'permissions': permissions
    })

    __sections = weight_sort(__sections)


def get_menu(sid: str, mid: str) -> dict:
    """Get a menu of a section.
    """
    section = get_section(sid)

    if not section:
        raise KeyError("Section '{}' is not exists.".format(sid))

    for m in section['children']:
        if m['mid'] == mid:
            return m


def add_menu(sid: str, mid: str, title: str, href: str='#', icon: str=None,
             label: str=None, label_class: str='primary', weight: int=0, permissions: tuple=()):
    """Add a menu to a section.
    """
    section = get_section(sid)

    if get_menu(sid, mid):
        raise KeyError("Menu '{}' already defined in section '{}'.".format(mid, sid))

    section['children'].append({
        'sid': sid,
        'mid': mid,
        'title': title,
        'href': href,
        'icon': icon,
        'label': label,
        'label_class': label_class,
        'weight': weight,
        'children': [],
        'permissions': permissions
    })

    section['children'] = weight_sort(section['children'])


def add_menu_child(sid: str, mid: str, title: str, href: str, weight: 0, permissions: tuple=()):
    """Add a child to the menu.
    """
    menu = get_menu(sid, mid)

    if not menu:
        raise KeyError("Menu '{}' is not defined in section '{}'.".format(mid, sid))

    menu['children'].append({
        'sid': sid,
        'mid': mid,
        'title': title,
        'href': href,
        'weight': weight,
        'permissions': permissions,
    })

    menu['children'] = weight_sort(menu['children'])


def render() -> str:
    """Render the admin sidebar.
    """
    aside_em = Aside(cls='main-sidebar')
    sidebar_section_em = Section(cls='sidebar')
    aside_em.append(sidebar_section_em)

    root_menu_ul = Ul(cls='sidebar-menu')
    sidebar_section_em.append(root_menu_ul)

    for section in _filter_permissions(deepcopy(__sections)):
        if not len(section['children']):
            continue

        root_menu_ul.append(Li(section['title'], cls='header'))

        # Building top level menu item
        for menu in section['children']:
            if menu['children']:
                # TODO
                pass
            else:
                href = menu['href']
                a = A(href=href)
                if menu['icon']:
                    a.append(I(cls=menu['icon']))
                a.append(Span(menu['title']))
                if menu['label']:
                    label_class = 'label pull-right label-' + menu['label_class']
                    a.append(Span(menu['label'], cls=label_class))
                li = Li()
                if href.find(router.current_url()) >= 0:
                    li.set_attr('cls', 'active')
                root_menu_ul.append(li.append(a))

    return aside_em.render()


def _filter_permissions(container: list) -> list:
    for k, item in enumerate(container):
        if isinstance(item, dict):
            if not _check_permissions(item):
                del container[k]
            elif 'children' in item:
                _filter_permissions(item['children'])

    return container


def _check_permissions(container: dict) -> bool:
    user = auth_manager.get_current_user()
    if user.is_anonymous():
        return False

    for p in container['permissions']:
        if p == '*':
            return True
        elif user.has_permission(p):
            return True

    return False
