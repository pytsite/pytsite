"""Sitemap Builder
"""
import gzip as _gzip
from datetime import datetime as _datetime
from lxml import etree as _etree
from pytsite import validation as _validation, util as _util

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class _FileWriterMixin:
    def write(self, path: str, compress=False) -> str:
        """Write the sitemap's XML code into file.
        """
        if compress:
            with _gzip.open(path + '.gz', 'wt') as f:
                f.write(str(self))
            return path + '.gz'
        else:
            with open(path, 'wt') as f:
                f.write(str(self))
            return path


class Sitemap(_FileWriterMixin):
    """Sitemap.
    """
    def __init__(self):
        """Init.
        """
        self._urls = []

    def add_url(self, url: str, lastmod: _datetime=None, changefreq: str='never', priority: float=0.5):
        """Add an URL to the sitemap.
        """
        valid_freq = ('always', 'hourly', 'daily', 'weekly', 'monthly', 'yearly', 'never')
        if changefreq and changefreq not in valid_freq:
            raise AttributeError('changefreq must be one of the following: ' + repr(valid_freq))

        _validation.rule.Url(url).validate()

        self._urls.append({
            'loc': url,
            'changefreq': changefreq,
            'lastmod': lastmod,
            'priority': str(priority)
        })

    def __str__(self):
        """Generate sitemap's XML.
        """
        root_em = _etree.Element('urlset', xmlns='http://www.sitemaps.org/schemas/sitemap/0.9')

        for url in self._urls:
            url_em = _etree.Element('url')

            loc_em = _etree.Element('loc')
            loc_em.text = url['loc']
            url_em.append(loc_em)

            changefreq_em = _etree.Element('changefreq')
            changefreq_em.text = url['changefreq']
            url_em.append(changefreq_em)

            priority_em = _etree.Element('priority')
            priority_em.text = url['priority']
            url_em.append(priority_em)

            lastmod_em = _etree.Element('lastmod')
            lastmod_em.text = _util.w3c_datetime_str(url['lastmod'], True)
            url_em.append(lastmod_em)

            root_em.append(url_em)

        return _etree.tostring(root_em, pretty_print=True, encoding='utf-8', xml_declaration=True).decode('utf-8')

    def __len__(self) -> int:
        """Get number of added locations.
        """
        return len(self._urls)


class Index(_FileWriterMixin):
    """Sitemap Index.
    """
    def __init__(self):
        """Init.
        """
        self._urls = []

    def add_url(self, url: str, lastmod: _datetime=None):
        """Add an URL to the sitemap index.
        """
        self._urls.append({
            'loc': _validation.rule.Url(url).validate(),
            'lastmod': lastmod,
        })

    def __str__(self):
        """Generate sitemap index's XML.
        """
        root_em = _etree.Element('sitemapindex', xmlns='http://www.sitemaps.org/schemas/sitemap/0.9')

        for url in self._urls:
            sitemap_em = _etree.Element('sitemap')

            # Loc
            loc_em = _etree.Element('loc')
            loc_em.text = url['loc']
            sitemap_em.append(loc_em)

            # Lastmod
            lastmod_em = _etree.Element('lastmod')
            lastmod_em.text = _util.w3c_datetime_str(url['lastmod'], True)
            sitemap_em.append(lastmod_em)

            # Add 'sitemap' to the 'sitemapindex' root
            root_em.append(sitemap_em)

        return _etree.tostring(root_em, pretty_print=True, encoding='utf-8', xml_declaration=True).decode('utf-8')

    def __len__(self) -> int:
        """Get number of added locations.
        """
        return len(self._urls)
