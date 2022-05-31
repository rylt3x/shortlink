# Telegram bot lib
from telegram.utils.request import Request
from telegram import Update
from telegram import Bot
from telegram.ext import ConversationHandler
from telegram import ReplyKeyboardMarkup
from telegram.ext import CommandHandler
from telegram.ext import Updater
from telegram.ext import CallbackContext
from telegram.ext import Filters
from telegram.ext import MessageHandler
from telegram.ext import CallbackQueryHandler
from telegram import ParseMode

from .source import handlers


# Django
from django.core.management import BaseCommand
from project import settings


class Command(BaseCommand):
    help = 'Telegram short link bot'

    def handle(self, *args, **options):
        self.stdout.write('Dating bot command started')

        req = Request(
            con_pool_size=8,
            connect_timeout=3
        )
        bot = Bot(
            token=settings.BOT_TOKEN,
            request=req
        )
        updater = Updater(
            bot=bot,
            use_context=True,
        )

        updater.dispatcher.add_handler(CommandHandler('start', handlers.start_handler))
        updater.dispatcher.add_handler(ConversationHandler(
            entry_points=[MessageHandler(Filters.text('Сократить ссылку'), callback=handlers.srt_start)],
            states={
                1: [MessageHandler(Filters.text, handlers.srt_register)]
            },
            fallbacks=[MessageHandler(Filters.text('завершить'), handlers.srt_force_end)]
        ))

        updater.start_polling()
        updater.idle()
