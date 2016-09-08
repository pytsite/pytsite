"""PytSite Native Comments Widget.
"""
from pytsite import widget as _pytsite_widget, html as _html, tpl as _tpl, auth as _auth, comments as _comments, \
    lang as _lang

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class Comments(_pytsite_widget.Abstract):
    def __init__(self, uid: str, **kwargs):
        """Init.
        """
        if 'title' not in kwargs:
            kwargs['title'] = _lang.t('pytsite.comments_native@comments')

        super().__init__(uid, **kwargs)

        self._thread_id = kwargs.get('thread_id')
        if not self._thread_id:
            raise RuntimeError("Widget '{}': thread_id is not specified.".format(self.name))

        self._css = 'comments-native'
        self._data['comments_load_ep'] = 'comments/comments'
        self._data['comment_submit_ep'] = 'comments/comment'
        self._data['thread_id'] = self._thread_id
        self._data['max_depth'] = _comments.get_comment_max_depth()
        self._data['create_permission'] = _comments.get_permissions(driver_name='native')['create']

        self._assets.extend([
            'pytsite.comments_native@css/widget.css',
            'pytsite.comments_native@js/widget.js',
        ])

    @property
    def comment_submit_ep(self) -> str:
        return 'pytsite.comments@comment'

    @property
    def comment_body_max_length(self) -> int:
        return _comments.get_comment_body_max_length()

    def get_html_em(self, **kwargs) -> _html.Element:
        return _html.TagLessElement(_tpl.render('pytsite.comments_native@widget', {
            'current_user': _auth.get_current_user(),
            'widget': self,
        }))
