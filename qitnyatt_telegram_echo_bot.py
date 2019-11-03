#!/usr/bin/env python
# -*- coding: utf-8 -*-


import logging

# noinspection PyPackageRequirements
from telegram.ext import CommandHandler
# noinspection PyPackageRequirements
from telegram.ext import Filters
# noinspection PyPackageRequirements
from telegram.ext import MessageHandler
# noinspection PyPackageRequirements
from telegram.ext import Updater

FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
logging.basicConfig(
    format=FORMAT,
    level=logging.INFO
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
    token = input('TOKEN:')
    updater = Updater(token, use_context=True)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('help', help_))
    dispatcher.add_handler(MessageHandler(Filters.text, echo))
    dispatcher.add_error_handler(error)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
