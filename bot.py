#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Simple Bot to reply to Telegram messages.
This program is dedicated to the public domain under the CC0 license.
This Bot uses the Updater class to handle the bot.
First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
Usage:
Basic inline bot example. Applies different text transformations.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""
import configparser

from uuid import uuid4

from telegram.utils.helpers import escape_markdown

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram import InlineQueryResultArticle, ParseMode, InputTextMessageContent
from telegram.ext import Updater, InlineQueryHandler, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
import logging

import time
import datetime
import crawler


# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

start_welcome = ('Здравствуйте!\n\n'
    '上坂すみれ です! I can push you my latest LINE Blog images! （＾∇＾）\n\n'
    'If you need command reference, please type in /help.\n\n'
    'До встречи!\n'
    'СУМИРЭ すみれ')

help_ref = ('Command Refernce:\n\n'
    '/start - start inline-keyboard-button mode operation\n'
    '/crawl - crawl the images of the latest article only\n'
    '/crawl_all - crawl the images of the latest three articles\n'
    '/mainpage - get the mainpage URL\n'
    '/archive - get the specific archive page URL FORMAT: /archive [YEAR]-[MONTH] e.g. /archive 2018-12\n'
    '/update_check - check out whether the blog updated today')
blog_url = 'https://lineblog.me/uesaka_sumire/'
time_args = []


# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.

############################### Bot ############################################

# def push(bot, job):
    #"""Send the push message."""
    # if crawler.date_push_compare() == True:
    #     urls = crawler.specific_parse_and_download(blog_url)
    #     for url in urls:
    #         job.context.message.reply_text(url)
    # else:
    #     job.context.message.reply_text("No Update Today")


# def timer(bot, update, job_queue):
    # day_frequency = 1
    # day_time = datetime.time(hour=5, minute=14, second=0)
    # job = job_queue.run_daily(callback=push, 
                              # time=day_time, 
                              # days=day_frequency, 
                              # context=update)


def start(bot, update):
    """Send a message when the command /start is issued."""
    update.message.reply_text(main_menu_message(), reply_markup=main_menu_keyboard())

    
def main_menu(bot, update):
    query = update.callback_query
    bot.edit_message_text(text=main_menu_message(),
                          chat_id=query.message.chat_id, 
                          message_id=query.message.message_id,
                          reply_markup=main_menu_keyboard())

def archive_menu(bot, update):
    query = update.callback_query
    bot.edit_message_text(text=archive_menu_message(),
                          chat_id=query.message.chat_id,
                          message_id=query.message.message_id,
                          reply_markup=archive_menu_keyboard())

def archive_submenu(bot, update):
    query = update.callback_query
    time_args.clear()
    time_args.append(query.data)
    bot.edit_message_text(text=archive_submenu_message(),
                          chat_id=query.message.chat_id,
                          message_id=query.message.message_id,
                          reply_markup=archive_submenu_keyboard())

def month_button(bot, update):
    query = update.callback_query

    time_args.append(query.data)
    url_seq = (blog_url, 'archives/', time_args[0], '-',time_args[1], '.html')
    split_sign = ''
    archive_url = str(split_sign.join(url_seq))

    bot.edit_message_text(text="Archive URL: " + archive_url,
                          chat_id=query.message.chat_id,
                          message_id=query.message.message_id)

def button(bot, update):
    query = update.callback_query
    bot.edit_message_text(text="Selected Command: {}".format(query.data),
                          chat_id=query.message.chat_id,
                          message_id=query.message.message_id)

############################ Keyboards #########################################

# def build_menu(buttons,
#                n_cols,
#                header_buttons=None,
#                footer_buttons=None):
#     menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
#     if header_buttons:
#         menu.insert(0, header_buttons)
#     if footer_buttons:
#         menu.append(footer_buttons)
#     return menu

def main_menu_keyboard():
    keyboard = [[InlineKeyboardButton("Crawl", callback_data='/crawl'),
                 InlineKeyboardButton("Crawl All", callback_data='/crawl_all')],

                [InlineKeyboardButton("Main Page", url=blog_url),
                 InlineKeyboardButton("Archive", callback_data='archive')],

                [InlineKeyboardButton("Blog Update Check", callback_data='/update_check')]]
    return InlineKeyboardMarkup(keyboard)

def archive_menu_keyboard():
    # archive_buttons = ["2011", "2012", "2013", "2014", "2015", "2016", "2017", "2018", "2019", "Main Menu"]
    # button_list = [[KeyboardButton(button)] for button in archive_buttons]
    # keyboard = InlineKeyboardMarkup(util.build_menu(button_list, n_cols=2))
    keyboard =[[InlineKeyboardButton('2019', callback_data='2019'),
                InlineKeyboardButton('2018', callback_data='2018')],

               [InlineKeyboardButton('2017', callback_data='2017'),
                InlineKeyboardButton('2016', callback_data='2016')],

               [InlineKeyboardButton('2015', callback_data='2015'),
                InlineKeyboardButton('2014', callback_data='2014')],

               [InlineKeyboardButton('2013', callback_data='2013'),
                InlineKeyboardButton('2012', callback_data='2012')],

               [InlineKeyboardButton('2011', callback_data='2011'),
                InlineKeyboardButton('Main Menu', callback_data='main')]]
    return InlineKeyboardMarkup(keyboard)

def archive_submenu_keyboard():
    keyboard =[[InlineKeyboardButton('01', callback_data='01'),
                InlineKeyboardButton('02', callback_data='02')],
               
               [InlineKeyboardButton('03', callback_data='03'),
                InlineKeyboardButton('04', callback_data='04')],

               [InlineKeyboardButton('05', callback_data='05'),
                InlineKeyboardButton('06', callback_data='06')],

               [InlineKeyboardButton('07', callback_data='07'),
                InlineKeyboardButton('08', callback_data='08')],
                
               [InlineKeyboardButton('09', callback_data='09'),
                InlineKeyboardButton('10', callback_data='10')],
                
               [InlineKeyboardButton('11', callback_data='11'),
                InlineKeyboardButton('12', callback_data='12')],

                [InlineKeyboardButton('Choose Year', callback_data='archive')]]
    return InlineKeyboardMarkup(keyboard)

############################# Messages #########################################

def main_menu_message():
    return 'Choose the option in main menu: '

def archive_menu_message():
    return 'Choose the Year: '

def archive_submenu_message():
    return 'Choose the Month: '

    
############################# Components #########################################

def help(bot, update):
    """Send a message when the command /help is issued."""
    update.message.reply_text(help_ref)


def inlinequery(bot, update):
    """Handle the inline query."""
    query = update.inline_query.query
    results = [
        InlineQueryResultArticle(
            id=uuid4(),
            title="Caps",
            input_message_content=InputTextMessageContent(
                query.upper())),
        InlineQueryResultArticle(
            id=uuid4(),
            title="Bold",
            input_message_content=InputTextMessageContent(
                "*{}*".format(escape_markdown(query)),
                parse_mode=ParseMode.MARKDOWN)),
        InlineQueryResultArticle(
            id=uuid4(),
            title="Italic",
            input_message_content=InputTextMessageContent(
                "_{}_".format(escape_markdown(query)),
                parse_mode=ParseMode.MARKDOWN))]

    update.inline_query.answer(results)


def crawl(bot, update):
	urls = crawler.specific_parse_and_download(blog_url)
	
	for url in urls:
		update.message.reply_text(url)
        # bot.send_photo(chat_id=update.message.chat_id, photo=url + '.jpg')


def crawl_all(bot, update):
    urls_webpage = crawler.whole_parse_and_download(blog_url)
    
    for urls in urls_webpage:
        for url in urls:
            update.message.reply_text(url)
            # bot.send_photo(chat_id=update.message.chat_id, photo=url + '.jpg')


def mainpage(bot, update):
	update.message.reply_text(blog_url)
	

def archive(bot, update, args): 
    url_seq = (blog_url, 'archives/', args[0], '.html')
    split_sign = ''
    archive_url = str(split_sign.join(url_seq))
    update.message.reply_text(archive_url)


def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)


def echo(bot, update):
    """Echo the user message."""
    update.message.reply_text(start_welcome)


def update_check(bot, update):
    if crawler.date_push_compare() == True:
        urls = crawler.specific_parse_and_download(blog_url)
        for url in urls:
            update.message.reply_text(url)
    else:
        update.message.reply_text("No Update Today")


############################# Main #########################################

def main():
    
    # Load data from config.ini file
    config = configparser.ConfigParser()
    config.read("config.ini")

    # Create the Updater and pass it your bot's token.
    TOKEN = (config['TELEGRAM']['ACCESS_TOKEN'])
    # TOKEN = config.get('TELEGRAM', 'ACCESS_TOKEN')
    updater = Updater(TOKEN)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher
    job_queue = updater.job_queue

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("crawl", crawl))
    dp.add_handler(CommandHandler("crawl_all", crawl_all))
    dp.add_handler(CommandHandler("mainpage", mainpage))
    # dp.add_handler(CommandHandler("archive", archive, pass_args=True))
    archive_handler = CommandHandler('archive', archive, pass_args=True)
    dp.add_handler(archive_handler)

    dp.add_handler(MessageHandler(Filters.text, echo))
    # dp.add_handler(MessageHandler(Filters.text, timer, pass_job_queue=True))
    dp.add_handler(CommandHandler("update_check", update_check))

    dp.add_handler(CallbackQueryHandler(button, pattern='/update_check'))
    dp.add_handler(CallbackQueryHandler(button, pattern='/crawl'))
    dp.add_handler(CallbackQueryHandler(button, pattern='/crawl_all'))

    dp.add_handler(CallbackQueryHandler(main_menu, pattern='main'))
    dp.add_handler(CallbackQueryHandler(archive_menu, pattern='archive'))

    dp.add_handler(CallbackQueryHandler(archive_submenu, pattern='2011'))
    dp.add_handler(CallbackQueryHandler(archive_submenu, pattern='2012'))
    dp.add_handler(CallbackQueryHandler(archive_submenu, pattern='2013'))
    dp.add_handler(CallbackQueryHandler(archive_submenu, pattern='2014'))
    dp.add_handler(CallbackQueryHandler(archive_submenu, pattern='2015'))
    dp.add_handler(CallbackQueryHandler(archive_submenu, pattern='2016'))
    dp.add_handler(CallbackQueryHandler(archive_submenu, pattern='2017'))
    dp.add_handler(CallbackQueryHandler(archive_submenu, pattern='2018'))
    dp.add_handler(CallbackQueryHandler(archive_submenu, pattern='2019'))

    dp.add_handler(CallbackQueryHandler(month_button, pattern='01'))
    dp.add_handler(CallbackQueryHandler(month_button, pattern='02'))
    dp.add_handler(CallbackQueryHandler(month_button, pattern='03'))
    dp.add_handler(CallbackQueryHandler(month_button, pattern='04'))
    dp.add_handler(CallbackQueryHandler(month_button, pattern='05'))
    dp.add_handler(CallbackQueryHandler(month_button, pattern='06'))
    dp.add_handler(CallbackQueryHandler(month_button, pattern='07'))
    dp.add_handler(CallbackQueryHandler(month_button, pattern='08'))
    dp.add_handler(CallbackQueryHandler(month_button, pattern='09'))
    dp.add_handler(CallbackQueryHandler(month_button, pattern='10'))
    dp.add_handler(CallbackQueryHandler(month_button, pattern='11'))
    dp.add_handler(CallbackQueryHandler(month_button, pattern='12'))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(InlineQueryHandler(inlinequery))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Block until the user presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()