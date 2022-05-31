from django.contrib import admin
from django.urls import path
from django.contrib.sitemaps.views import sitemap
from.sitemaps import IndexSitemap, PageSitemap

from . import views
from .models import SourceLink, Page

source_links = SourceLink.objects.all()

sitemaps = {
    'home': IndexSitemap,
    'pages': PageSitemap,
}

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<slug:slug>/', views.RedirectView.as_view(), name='redirect_url'),
    path('robots.txt', views.robots_txt, name='robots'),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('yandex_8fbb6423591a78c8.html', views.yandex_webmaster, name='yandex_webmaster'),
]

for page in Page.objects.all():
    urlpatterns += [
        path('page/' + page.slug, views.IndexView.as_view(), name=page.slug),
    ]
