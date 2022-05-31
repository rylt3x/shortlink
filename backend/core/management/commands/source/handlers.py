from telegram import Update, ParseMode
from telegram.ext import CallbackContext, ConversationHandler

from core.management.commands.source import keyboards
from project import settings
from core.utils import create_short_link


def start_handler(update: Update, context: CallbackContext):
    update.effective_message.reply_text('Привет', reply_markup=keyboards.start_keyboard)


def srt_start(update: Update, context: CallbackContext):
    update.message.reply_text('отправь ссылку')
    return 1


def srt_register(update: Update, context: CallbackContext):
    url = update.effective_message.text
    created_link, status = create_short_link(url)
    endpoint_url = settings.site_url+'/'+created_link

    if status == 'error':
        update.effective_message.reply_text('Некорректный url. Отправьте еще раз')
        return 1
    elif status == 'exists':
        update.effective_message.reply_text(f'Уже существует. Ссылка: <a href="{endpoint_url}">{endpoint_url}</a>', parse_mode=ParseMode.HTML)
        return ConversationHandler.END

    update.effective_message.reply_text(f'Ссылка создана: <a href="{endpoint_url}">{endpoint_url}</a>', parse_mode=ParseMode.HTML)
    return ConversationHandler.END


def srt_end(update: Update, context: CallbackContext):
    update.effective_message.reply_text('ссылка сокращена')
    return ConversationHandler.END


def srt_force_end(update: Update, context: CallbackContext):
    update.effective_message.reply_text('Принудительный выход')
    return ConversationHandler.END
