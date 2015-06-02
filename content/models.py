"""Content Models.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


from pytsite.core.odm.models import ODMModel
from pytsite.core.odm.fields import *
from pytsite.odm_ui.models import ODMUIMixin


class ContentModel(ODMModel, ODMUIMixin):

    def _setup(self):
        """_setup() hook.
        """
        self._define_field(StringField('title', not_empty=True))
        self._define_field(StringField('body'))
        self._define_field(StringField('description'))
        self._define_field(RefField('path', model='path', not_empty=True))
        self._define_field(DateTimeField('publish_time', not_empty=True))
        self._define_field(IntegerField('views_count'))
        self._define_field(IntegerField('comments_count'))
        self._define_field(RefsListField('images', model='image'))
        self._define_field(StringListField('video'))
        self._define_field(StringListField('links'))
        self._define_field(StringField('status', default='published', not_empty=True))
        self._define_field(RefsListField('localizations', model=self.model))
        self._define_field(RefField('author', model='user', not_empty=True))
        self._define_field(StringField('language', not_empty=True))
        self._define_field(RefsListField('tags', model='tag'))
        self._define_field(RefField('section', model='section'))
        self._define_field(RefField('location', model='location'))
        self._define_field(BoolField('starred'))
