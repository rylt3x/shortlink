from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from core import models


class PageSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 1

    def items(self):
        return models.Page.objects.all()

    def location(self, item):
        return f'/page/{item.slug}'

    def lastmod(self, obj):
        return obj.modified_at


class IndexSitemap(Sitemap):
    changefreq = 'never'
    priority = 1

    def items(self):
        return '/'

    def location(self, item):
        return ''

