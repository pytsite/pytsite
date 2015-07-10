"""Admin Sidebar.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from pytsite import auth as _auth
from pytsite.core import util as _util, html as _html, lang as _lang, router as _router


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

    __sections = _util.weight_sort(__sections)


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
             label: str=None, label_class: str='primary', weight: int=0, permissions: tuple=(), replace=False):
    """Add a menu to a section.
    """
    section = get_section(sid)
    if not section:
        raise KeyError("Section '{}' is not exists.".format(sid))

    if get_menu(sid, mid):
        if replace:
            del_menu(sid, mid)
        else:
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

    section['children'] = _util.weight_sort(section['children'])


def del_menu(sid: str, mid: str):
    """delete menu from section.
    """
    section = get_section(sid)
    if not section:
        raise KeyError("Section '{}' is not exists.".format(sid))

    replace = []
    for m in section['children']:
        if m['mid'] != mid:
            replace.append(m)

    section['children'] = replace


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

    menu['children'] = _util.weight_sort(menu['children'])


def render() -> str:
    """Render the admin sidebar.
    """
    aside_em = _html.Aside(cls='main-sidebar')
    sidebar_section_em = _html.Section(cls='sidebar')
    aside_em.append(sidebar_section_em)

    root_menu_ul = _html.Ul(cls='sidebar-menu')
    sidebar_section_em.append(root_menu_ul)

    from copy import deepcopy
    for section in _filter_permissions(deepcopy(__sections)):
        if not len(section['children']):
            continue

        root_menu_ul.append(
            _html.Li(_lang.t(section['title']), cls='header', data_section_weight=section['weight']))

        # Building top level menu item
        for menu in section['children']:
            if menu['children']:
                # TODO
                pass
            else:
                # Link
                href = menu['href']
                a = _html.A(href=href)

                # Icon
                if menu['icon']:
                    a.append(_html.I(cls=menu['icon']))

                # Title
                a.append(_html.Span(_lang.t(menu['title'])))

                # Label
                if menu['label']:
                    label_class = 'label pull-right label-' + menu['label_class']
                    a.append(_html.Span(_lang.t(menu['label']), cls=label_class))

                # List element
                li = _html.Li(data_menu_weight=menu['weight'])

                # 'active' CSS class
                current_url = _router.current_url()
                if not current_url.endswith('/admin') and current_url.find(href) >= 0:
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
    user = _auth.get_current_user()
    if user.is_anonymous:
        return False

    for p in container['permissions']:
        if p == '*':
            return True
        elif user.has_permission(p):
            return True

    return False
