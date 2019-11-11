#!/usr/bin/env python
# -*- coding: utf-8 -*-


import logging

# noinspection PyPackageRequirements
import environ
# noinspection PyPackageRequirements
from telegram.ext import CommandHandler
# noinspection PyPackageRequirements
from telegram.ext import Filters
# noinspection PyPackageRequirements
from telegram.ext import MessageHandler
# noinspection PyPackageRequirements
from telegram.ext import Updater

env = environ.Env(
    qitnyatt_telegram_echo_bot__MODE=(str, 'prod'),
    qitnyatt_telegram_echo_bot__BOT_PORT=(int, '8443'),
    qitnyatt_telegram_echo_bot__USE_HEROKU=(bool, False),
    qitnyatt_telegram_echo_bot__HEROKU_APP_NAME=(str, '<HEROKU_APP_NAME>'),
    qitnyatt_telegram_echo_bot__TOKEN=(str, '<TOKEN>'),
)

environ.Env.read_env()

MODE = env('qitnyatt_telegram_echo_bot__MODE')
USE_HEROKU = env('qitnyatt_telegram_echo_bot__USE_HEROKU')
if USE_HEROKU:
    PORT = env('PORT')
    HEROKU_APP_NAME = env('qitnyatt_telegram_echo_bot__HEROKU_APP_NAME')
else:
    PORT = env('qitnyatt_telegram_echo_bot__BOT_PORT')
TOKEN = env('qitnyatt_telegram_echo_bot__TOKEN')

FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
logging.basicConfig(
    format=FORMAT,
    level=logging.DEBUG if MODE == 'dev' else logging.INFO
)

logger = logging.getLogger(__name__)


# noinspection PyUnusedLocal
def start(update, context):
    first_name = update.message.from_user.first_name
    last_name = update.message.from_user.last_name
    update.message.reply_text(f'Hello, {first_name} {last_name}.')


# noinspection PyUnusedLocal
def help_(update, context):
    update.message.reply_text('sorry i can\'t help you.')


# noinspection PyUnusedLocal
def echo(update, context):
    update.message.reply_text(f'>>> {update.message.text}')


def error(update, context):
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    updater = Updater(TOKEN, use_context=True)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('help', help_))
    dispatcher.add_handler(MessageHandler(Filters.text, echo))
    dispatcher.add_error_handler(error)

    if MODE == 'dev':
        updater.start_polling()
        updater.idle()
    elif MODE == 'prod':
        if USE_HEROKU:
            updater.start_webhook(
                listen='0.0.0.0',
                port=PORT,
                url_path=TOKEN
            )
            updater.bot.set_webhook(
                f'https://{HEROKU_APP_NAME}.herokuapp.com/{TOKEN}'
            )
        else:
            logger.fatal(NotImplemented)
            exit(1)
        updater.idle()
    else:
        logger.fatal('No MODE specified!')
        exit(1)


if __name__ == '__main__':
    main()
