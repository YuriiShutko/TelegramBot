from telegram import Bot
from telegram import Update
from telegram import InlineKeyboardButton  # Отвечает за одну клавишу в клавиатуре
from telegram import InlineKeyboardMarkup  # Вся клавиатура вместе
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler
from telegram.ext import CallbackContext
from telegram.ext import Filters
from telegram.ext import CallbackQueryHandler  # Обработчик события нажатия на клавишу
from config.config import TELEGRAM_TOKEN


def do_start(update: Update,
             context: CallbackContext):  # update - экземпляр класса Updater (так будут доступны подсказки)
    """
    Обработчик событий (команды) от телеграма
    """
    first_name = update.message.chat.first_name
    context.bot.send_message(chat_id=update.message.chat_id, text='Привет, {} :)'.format(first_name))


def do_stop(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.message.chat_id, text='Пока')


def do_echo(update: Update, context: CallbackContext):
    """
    Функция, которая обрабатывает все входящие сообщения
    """
    text = update.message.text  # Получаем текст того, что нам написали
    context.bot.send_message(chat_id=update.message.chat_id, text=text)


def do_caps(update: Update, context: CallbackContext):
    arguments = ' '.join(context.args).upper()
    context.bot.send_message(chat_id=update.message.chat_id, text=arguments)


def unknown(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.message.chat_id, text='Я не знаю такой команды)')


def main():
    """
    Основная функция
    """
    updater = Updater(token=TELEGRAM_TOKEN, use_context=True)  # Создаем updater как экземпляр класса Updater

    # Добавляем обработчик команд
    start_handler = CommandHandler('start', do_start)
    stop_handler = CommandHandler('stop', do_stop)
    caps_handler = CommandHandler('caps', do_caps)
    unknown_handler = MessageHandler(Filters.command, unknown)
    message_handler = MessageHandler(Filters.text, do_echo)

    # Зарегистрируем обработчик в диспетчере который будет сортировать обновления извлеченные в Updater в соответствии
    # с зарегистрированными обработчиками и доставлять их в функцию обратного вызова callback

    updater.dispatcher.add_handler(start_handler)
    updater.dispatcher.add_handler(message_handler)
    updater.dispatcher.add_handler(stop_handler)
    updater.dispatcher.add_handler(caps_handler)
    updater.dispatcher.add_handler(unknown_handler)
    # Запускаем скачивание обновлений из телеграма
    updater.start_polling()
    # Указываем Updater, чтоб он не закрывался до тех пор пока не обработаются все updates и чтобы код работал до тех
    # пор пока мы сами не захотим его отключить
    updater.idle()


# Пишем код, чтобы наш бот запускался
if __name__ == '__main__':
    main()
