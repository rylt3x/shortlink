from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import resolve
from django.views.generic.base import View

from .utils import create_short_link

import requests

from core import models
from project import settings

def send_message(text: str):
    import requests
    BOT_TOKEN = "2121695191:AAGB44cI9p1uWusJf7jLa3C4A6EDd7MzesE"
    url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage?chat_id={439992907}&text={text}'
    res = requests.get(url)


class IndexView(View):

    def get(self, request):
        request.session.save()
        generated_links = models.SourceLink.objects.filter(session=request.session.session_key).order_by('-id')[:5]

        page_data = {
            'title': 'Сервис сокращения ссылок | Yuup.pw',
            'description': 'Сократить ссылку онлайн бесплатно на yuup.pw. Короткая ссылка для Вк, Ватсап, Гугл, Яндекс, Инстаграм, Твиттер, Ютуб и других сервисов.',
            'h1': 'Сервис сокращения ссылок'
        }

        # Получаем имя urlpattern'а который сработал
        slug = resolve(request.path_info).url_name
        page_object = models.Page.objects.filter(slug=slug).first()
        if page_object:
            if page_object.title:
                page_data['title'] = page_object.title.capitalize()
            if page_object.description:
                page_data['description'] = page_object.description
            if page_object.headline_h1:
                page_data['h1'] = page_object.headline_h1

        context_data = {'data': generated_links, 'page_data': page_data}
        return render(request, 'index.html', context_data)

    def post(self, request):
        source_link = request.POST.get('source_link')
        session_key = request.session.session_key
        created_link, status = create_short_link(source_link, session_key)
        if status == 'error':
            return JsonResponse({'status': 'error', 'link': 'null'})

        return JsonResponse({'status': '200', 'link': created_link})


class RedirectView(View):
    def get(self, request, *args, **kwargs):
        forward_url = get_object_or_404(models.SourceLink, source_link=kwargs.get('slug'))
        ip = request.META.get('HTTP_X_REAL_IP', "")
        user_agent = request.META.get('HTTP_USER_AGENT')
        if forward_url:
            models.LinkFollow.objects.create(link_pair=forward_url, ip_address=ip, user_agent=user_agent)

        return redirect(forward_url.forward_link)


def robots_txt(request):
    return render(request, 'robots.txt', content_type='text/plain')


def yandex_webmaster(request):
    return render(request, 'yandex_webmaster.html', content_type='text/html')

