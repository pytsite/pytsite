"""Content Console Commands.
"""
from random import shuffle as _shuffle, random as _random, randint as _randint
import requests as _requests
from pytsite import image as _image, auth as _auth, console as _console, lang as _lang, events as _events, \
    validation as _validation
from . import _api

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class Generate(_console.command.Abstract):
    """Abstract command.
    """
    li_url = 'http://loripsum.net/api/prude/'
    lp_url = 'http://pipsum.com/1024x768'

    def get_name(self) -> str:
        """Get command's name.
        """
        return 'content:generate'

    def get_description(self) -> str:
        """Get command's description.
        """
        return _lang.t('pytsite.content@console_generate_command_description')

    def get_options_help(self) -> str:
        """Get help for command's options.
        """
        return '[--author=LOGIN] [--description-len=LEN] [--images=NUM] [--lang=LANG] [--num=NUM] [--no-html] ' \
               '[--no-tags] [--no-sections] [--short] [--title-len=LEN] --model=MODEL'

    def get_options(self) -> tuple:
        """Get command options.
        """
        return (
            ('model', _validation.rule.NonEmpty(msg_id='pytsite.content@model_is_required')),
            ('num', _validation.rule.Integer()),
            ('images', _validation.rule.Integer()),
            ('title-len', _validation.rule.Integer()),
            ('description-len', _validation.rule.Integer()),
            ('lang', _validation.rule.Regex(pattern='^[a-z]{2}$')),
            ('no-html', _validation.rule.Dummy()),
            ('short', _validation.rule.Dummy()),
            ('author', _validation.rule.Dummy()),
            ('no-tags', _validation.rule.Dummy()),
            ('no-sections', _validation.rule.Dummy()),
        )

    def execute(self, args: tuple=(), **kwargs):
        """Execute teh command.
        """
        model = kwargs['model']

        # Checking if the content model registered
        if not _api.is_model_registered(model):
            raise _console.error.Error("'{}' is not a registered content model.".format(model))

        author_login = kwargs.get('author')
        num = int(kwargs.get('num', 10))
        images_num = int(kwargs.get('images', 1))
        language = kwargs.get('lang', _lang.get_current())
        no_html = kwargs.get('no-html')
        short = kwargs.get('short')
        no_tags = kwargs.get('no-tags')
        no_sections = kwargs.get('no-sections')

        if short:
            self.li_url += 'short/'

        # Generate content entities
        for m in range(0, num):
            entity = _api.dispense(model)

            # Author
            if author_login:
                author = _auth.get_user(author_login)
                if not author:
                    raise _console.error.Error("'{}' is not a registered user.".format(author_login))
                entity.f_set('author', author)
            else:
                user_finder = _auth.find_users()
                users_count = user_finder.count()
                if not users_count:
                    raise _lang.t('pytsite.content@no_users_found')
                entity.f_set('author', user_finder.skip(_randint(0, users_count - 1)).first())

            # Title
            entity.f_set('title', self._generate_title(int(kwargs.get('title-len', 7))))

            # Description
            if entity.has_field('description'):
                entity.f_set('description', self._generate_title(int(kwargs.get('description-len', 28))))

            # Tags
            if not no_tags and entity.has_field('tags'):
                # Generate tags
                tags = list(_api.get_tags(language=language))
                if len(tags) < 10:
                    for n in range(0, 10):
                        tags.append(_api.dispense_tag(self._generate_title(1), language=language).save())

                _shuffle(tags)
                entity.f_set('tags', tags[:5])

            # Section
            if not no_sections and entity.has_field('section'):
                # Generate sections
                sections = list(_api.get_sections(language))
                if not len(sections):
                    for i in range(0, 3):
                        title = self._generate_title(1)
                        section = _api.dispense_section(title, language=language).save()
                        sections.append(section)
                        _console.print_info(_lang.t('pytsite.content@new_section_created', {'title': title}))

                _shuffle(sections)
                entity.f_set('section', sections[0])

            # Body
            body_parts_num = images_num or 3
            body = []
            for n in range(1, body_parts_num + 1):
                if no_html:
                    body.append(_requests.get(self.li_url + '/plaintext/').content.decode('utf-8'))
                else:
                    body.append(_requests.get(self.li_url + '/decorate/link/ul/ol/dl/bq/').content.decode('utf-8'))
                    body.append('\n<p>[img:{}]</p>\n'.format(n))
                    body.append(_requests.get(self.li_url).content.decode('utf-8'))
            entity.f_set('body', ''.join(body))

            # Images
            if entity.has_field('images') and images_num:
                for n in range(0, images_num):
                    entity.f_add('images', _image.create(self.lp_url))

            entity.f_set('status', 'published')
            entity.f_set('views_count', int(_random() * 1000))
            entity.f_set('comments_count', int(_random() * 100))
            entity.f_set('language', language)

            _events.fire('pytsite.content.generate', entity=entity)

            entity.save()

            _console.print_info(_lang.t('pytsite.content@new_content_created', {'title': entity.title}))

    def _generate_title(self, max_words=7) -> str:
        title = str(_requests.get(self.li_url + '/1/plaintext/verylong').content.decode('utf-8')).strip()

        for s in [',', '.', ':', ';', '?', '-']:
            title = title.replace(s, '')

        title = title.split(' ')
        _shuffle(title)
        title[0] = title[0].title()
        title = ' '.join(title[0:max_words])

        return title
