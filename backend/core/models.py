import datetime


from django.db import models


class SourceLink(models.Model):
    source_link = models.CharField(verbose_name='slug', max_length=16, unique=True)
    forward_link = models.URLField(verbose_name='forward_link', max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    session = models.CharField(verbose_name='Сессия', max_length=128, null=True, blank=True)

    def __str__(self):
        return f'{self.source_link} to {self.forward_link}'

    class Meta:
        verbose_name = 'Ссылочная пара'
        verbose_name_plural = 'Ссылочные пары'
        indexes = [models.Index(fields=['id']), ]


class TelegramUser(models.Model):
    external_id = models.CharField(verbose_name='Telegram id', max_length=32)
    username = models.CharField(verbose_name='Username', max_length=128)
    first_name = models.CharField(verbose_name='Имя', max_length=32)
    last_name = models.CharField(verbose_name='Фамилия', max_length=32)
    short_links = models.ForeignKey(SourceLink, on_delete=models.CASCADE, related_name='tg_user')

    class Meta:
        verbose_name = 'Пользователь Telegram'
        verbose_name_plural = 'Пользователи Telegram'
        indexes = [models.Index(fields=['external_id']), ]


class LinkFollow(models.Model):
    link_pair = models.ForeignKey(SourceLink, related_name='links', on_delete=models.CASCADE)
    ip_address = models.GenericIPAddressField(verbose_name='Ip адрес', default='0.0.0.0')
    user_agent = models.TextField(verbose_name='User-agent', null=True, default=None)
    created_at = models.DateTimeField(verbose_name='Время перехода', auto_now_add=True)

    def __str__(self):
        return f'{self.ip_address} | {self.created_at.strftime("%m/%d/%Y %H:%M:%S")}'

    class Meta:
        verbose_name = 'Переход по ссылке'
        verbose_name_plural = 'Переходы по ссылкам'


class Page(models.Model):
    title = models.CharField(verbose_name='Тег Title', max_length=128)
    slug = models.SlugField(verbose_name='Ссылка', max_length=128)
    description = models.TextField(verbose_name='Тег description', max_length=255, null=True, blank=True)
    headline_h1 = models.CharField(verbose_name='Заголовок h1', max_length=64, null=True, blank=True)
    modified_at = models.DateTimeField(auto_now=True)

    @property
    def get_title(self):
        if self.title:
            return self.title.title()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Страница'
        verbose_name_plural = 'Страницы'
