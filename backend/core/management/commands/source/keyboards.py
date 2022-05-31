from telegram import ReplyKeyboardMarkup, KeyboardButton

start_keyboard = ReplyKeyboardMarkup(
    [
        [KeyboardButton('Сократить ссылку')]
    ],
    resize_keyboard=True
)