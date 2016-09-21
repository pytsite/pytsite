"""Admin Sidebar.
"""
from pytsite import auth as _auth, util as _util, html as _html, lang as _lang, router as _router, reg as _reg

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

_sections = []
_menus = {}
_last_section_weight = 0


def get_section(sid: str) -> dict:
    """Get section.
    """
    global _menus

    if sid not in _menus:
        return

    for s in _sections:
        if s['sid'] == sid:
            return s


def add_section(sid: str, title: str, weight: int = 0, permissions='*'):
    """Add a section.
    :param permissions: str|tuple
    """
    global _last_section_weight, _sections, _menus

    if get_section(sid):
        raise KeyError("Section '{}' is already defined.".format(sid))

    if not weight:
        weight = _last_section_weight + 100

    _last_section_weight = weight
    _sections.append({
        'sid': sid,
        'title': title,
        'weight': weight,
        'permissions': permissions
    })

    _menus[sid] = []
    _sections = _util.weight_sort(_sections)


def get_menu(sid: str, mid: str) -> dict:
    """Get a menu of a section.
    """
    section = get_section(sid)
    if not section:
        raise KeyError("Section '{}' is not defined.".format(sid))

    for m in _menus[sid]:
        if m['mid'] == mid:
            return m


def add_menu(sid: str, mid: str, title: str, href: str = '#', icon: str = None, label: str = None,
             label_class: str = 'primary', weight: int = 0, permissions=(), replace=False):
    """Add a menu to a section.
    :type permissions: str|tuple
    """
    global _menus

    section = get_section(sid)
    if not section:
        raise KeyError("Section '{}' is not defined.".format(sid))

    if get_menu(sid, mid):
        if replace:
            del_menu(sid, mid)
        else:
            raise KeyError("Menu '{}' already defined in section '{}'.".format(mid, sid))

    if isinstance(permissions, str):
        permissions = (permissions,)

    _menus[sid].append({
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

    _menus[sid] = _util.weight_sort(_menus[sid])


def del_menu(sid: str, mid: str):
    """delete menu from section.
    """
    section = get_section(sid)
    if not section:
        raise KeyError("Section '{}' is not defined.".format(sid))

    replace = []
    for m in _menus[sid]:
        if m['mid'] != mid:
            replace.append(m)

    _menus[sid] = replace


def render() -> _html.Aside:
    """Render the admin sidebar.
    """
    aside_em = _html.Aside(cls='main-sidebar')
    sidebar_section_em = _html.Section(cls='sidebar')
    aside_em.append(sidebar_section_em)

    root_menu_ul = _html.Ul(cls='sidebar-menu')
    sidebar_section_em.append(root_menu_ul)

    # Filtering permissions
    render_sections = []
    render_menus = {}
    for section in _sections:
        if not _check_permissions(section):
            continue
        render_sections.append(section)
        render_menus[section['sid']] = []
        for menu in _menus[section['sid']]:
            if _check_permissions(menu):
                render_menus[section['sid']].append(menu)

    # Remove empty sections from rendering
    render_sections = [s for s in render_sections if len(render_menus[s['sid']])]

    # Do actual rendering
    for section in render_sections:
        root_menu_ul.append(
            _html.Li(_lang.t(section['title']), cls='header', data_section_weight=section['weight']))

        # Building top level menu item
        for menu in render_menus[section['sid']]:
            # Link
            href = _router.url(menu['href'])
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
            abp = _reg.get('admin.base_path', '/admin')
            current_path = _router.current_path()
            if current_path != abp and href.endswith(current_path):
                li.set_attr('cls', 'active')

            root_menu_ul.append(li.append(a))

    return aside_em


def _check_permissions(item: dict) -> bool:
    user = _auth.get_current_user()
    if user.is_anonymous:
        return False

    if isinstance(item['permissions'], str) and item['permissions'] == '*':
        return True

    for p in item['permissions']:
        if p == '*':
            return True
        elif user.has_permission(p):
            return True

    return False
