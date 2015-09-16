"""Content Console Commands.
"""
from random import shuffle as _shuffle, random as _random, randint as _randint
import requests as _requests
from pytsite import image as _image, auth as _auth, console as _console, lang as _lang, events as _events
from . import _functions

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class Generate(_console.command.Abstract):
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

    @staticmethod
    def usage():
        """Print usage info.
        """
        _console.print_info('Usage: content:generate [--num=NUM] [--title-len=LEN] [--lang=LANG] [--no-html] [--short] '
                            '[--author=LOGIN] --model=MODEL ')

    def execute(self, **kwargs: dict):
        """Execute teh command.
        """
        model = kwargs.get('model')
        if not model:
            self.usage()
            return -1

        # Author
        author = None
        author_login = kwargs.get('author')
        if author_login:
            author = _auth.get_user(author_login)
            if not author:
                raise _console.Error("'{}' is not a registered user.".format(author_login))

        # Checking if the content model registered
        if not _functions.is_model_registered(model):
            raise _console.Error("'{}' is not a registered content model.".format(model))

        num = int(kwargs.get('num', 10))
        language = kwargs.get('lang', _lang.get_current_lang())
        no_html = kwargs.get('no-html')
        short = kwargs.get('short')

        if short:
            self.li_url += 'short/'

        # Generate sections
        sections = list(_functions.get_sections(language))
        if not len(sections):
            for m in range(0, 3):
                title = self._generate_title(1)
                section = _functions.create_section(title, language=language)
                sections.append(section)
                _console.print_info(_lang.t('pytsite.content@new_section_created', {'title': title}))

        # Generate tags
        tags = list(_functions.get_tags(language=language))
        if len(tags) < 10:
            for n in range(0, 10):
                tag = _functions.create_tag(self._generate_title(1), language=language)
                tags.append(tag)

        # Generate content entities
        for m in range(0, num):
            # Author
            if not author_login:
                user_finder = _auth.find_users()
                users_count = user_finder.count()
                if not users_count:
                    raise _lang.t('pytsite.content@no_users_found')

                author = user_finder.skip(_randint(0, users_count - 1)).first()

            # Title
            title = self._generate_title(int(kwargs.get('title-len', 7)))

            # Description
            description = self._generate_title()

            # Preparing sections and tags
            _shuffle(sections)
            _shuffle(tags)

            # Body and images
            body = []
            images = [_image.create(self.lp_url)]
            for n in range(2, 3 if short else 6):
                if no_html:
                    body.append(_requests.get(self.li_url + '/plaintext/').content.decode('utf-8'))
                else:
                    images.append(_image.create(self.lp_url))
                    body.append(_requests.get(self.li_url + '/decorate/link/ul/ol/dl/bq/').content.decode('utf-8'))
                    body.append('\n<p>[img:{}]</p>\n'.format(n))
                    body.append(_requests.get(self.li_url).content.decode('utf-8'))

            entity = _functions.create(model)
            entity.f_set('title', title)
            entity.f_set('description', description)
            entity.f_set('body', ''.join(body))
            entity.f_set('images', images)
            entity.f_set('tags', tags[:5])
            entity.f_set('author', author)
            entity.f_set('status', 'published')
            entity.f_set('views_count', int(_random() * 1000))
            entity.f_set('comments_count', int(_random() * 100))
            entity.f_set('language', language)

            if entity.has_field('section'):
                entity.f_set('section', sections[0])

            _events.fire('pytsite.content.console.generate', entity=entity)

            entity.save()

            _console.print_info(_lang.t('pytsite.content@new_content_created', {'title': title}))

    def _generate_title(self, max_words=7) -> str:
        title = str(_requests.get(self.li_url + '/1/plaintext/verylong').content.decode('utf-8')).strip()

        for s in [',', '.', ':', ';', '?', '-']:
            title = title.replace(s, '')

        title = title.split(' ')
        _shuffle(title)
        title[0] = title[0].title()
        title = ' '.join(title[0:max_words])

        return title
