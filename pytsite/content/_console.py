"""COntent Console Commands.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from random import shuffle as _shuffle, random as _random
import requests as _requests
from pytsite import image as _image, auth as _auth, console as _console, lang as _lang
from . import _functions


class Generate(_console._command.Abstract):
    """Abstract command.
    """
    li_url = 'http://loripsum.net/api/prude/'
    lp_url = 'http://lorempixel.com/1024/768/'

    def get_name(self) -> str:
        """Get command's name.
        """
        return 'content:generate'

    def get_description(self) -> str:
        """Get command's description.
        """
        return _lang.t('pytsite.content@console_command_description_generate')

    def usage(self):
        """Print usage info.
        """
        _console.print_info('Usage: content:generate [--num=NUM] [--title-len=LEN] --model=MODEL --author=LOGIN')

    def execute(self, **kwargs: dict):
        """Execute teh command.
        """
        model = kwargs.get('model')
        if not model:
            self.usage()
            return -1

        author_login = kwargs.get('author')
        if not author_login:
            self.usage()
            return -1

        if not _functions.is_model_registered(model):
            raise _console.Error("'{}' is not a registered content model.".format(model))

        author = _auth.get_user(author_login)
        if not author:
            raise _console.Error("'{}' is not a registered user.".format(author_login))

        # Generate sections
        sections = list(_functions.get_sections())
        if len(sections) < 3:
            for m in range(0, 3):
                title = self._generate_title(1)
                sections.append(_functions.create_section(title))
                _console.print_info(_lang.t('pytsite.content@new_section_created', {'title': title}))

        num = int(kwargs.get('num', 10))
        num = num if num > 0 else 10

        for m in range(0, num):
            title = self._generate_title(int(kwargs.get('title-len', 7)))
            description = self._generate_title()
            _shuffle(sections)

            body = []
            images = []
            for n in range(2, 6):
                images.append(_image.create(self.lp_url))
                body.append(_requests.get(self.li_url + '/decorate/link/ul/ol/dl/bq/').content.decode('utf-8'))
                body.append('\n<p>[img:{}]</p>\n'.format(n))
                body.append(_requests.get(self.li_url).content.decode('utf-8'))

            tags = []
            for n in range(0, 5):
                tag = _functions.create_tag(self._generate_title(1))
                tags.append(tag)

            entity = _functions.create(model)
            entity.f_set('title', title)
            entity.f_set('description', description)
            entity.f_set('body', ''.join(body))
            entity.f_set('images', images)
            entity.f_set('tags', tags)
            entity.f_set('author', author)
            entity.f_set('status', 'published')
            entity.f_set('views_count', int(_random() * 1000))
            entity.f_set('comments_count', int(_random() * 100))

            if entity.has_field('section'):
                entity.f_set('section', sections[0])

            entity.save()

            _console.print_info(_lang.t('pytsite.content@new_content_created', {'title': title}))

    def _generate_title(self, max_words=7) -> str:
        title = str(_requests.get(self.li_url + '/1//plaintext/verylong').content.decode('utf-8')).strip()

        for s in [',', '.', ':', ';', '?', '-']:
            title = title.replace(s, '')

        title = title.split(' ')
        _shuffle(title)
        title[0] = title[0].title()
        title = ' '.join(title[0:max_words])

        return title
