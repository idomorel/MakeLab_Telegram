import logging
import re
import datetime
from sys import exit
from signal import signal, SIGTERM, SIGINT
from os import path, remove, makedirs, listdir
from shutil import rmtree
from datetime import datetime, timedelta
from time import time, sleep, strptime, mktime, strftime
from threading import Thread, Lock
from operator import itemgetter
from collections import OrderedDict
from random import choice, randint
from telegram import (Update, InputMediaPhoto, InlineKeyboardButton, InlineKeyboardMarkup,
    ChatPermissions)
from telegram.ext import (CallbackContext, Updater, CommandHandler, MessageHandler, Filters,
    CallbackQueryHandler, Defaults)
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler


updater = None
files_config_list = []
to_delete_in_time_messages_list = []
to_delete_join_messages_list = []
new_users_list = []
th_0 = None
th_1 = None
force_exit = False

resuserid = 0
normalchatid = 0

SEND, REPLY = range(2)


# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)



# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hi!')


def help_command(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')



        

def add_lrm(str_to_modify):
    '''Add a Left to Right Mark (LRM) at provided string start'''
    barray = bytearray(b"\xe2\x80\x8e")
    str_to_modify = str_to_modify.encode("utf-8")
    for b in str_to_modify:
        barray.append(b)
    str_to_modify = barray.decode("utf-8")
    return str_to_modify

#def wait_for_user_answer()
 
# def key_inline_keyboard(update: Update, context: CallbackContext):
#     '''Inline Keyboard button pressed handler'''
#     bot = context.bot
#     query = update.callback_query
#     print(query)
    # Confirm query received
    # try:
    #     bot.answer_callback_query(query.id)
    # except Exception as e:
    #     print("[{}] {}".format(query.message.chat_id, str(e)))
    # Convert query provided data into list
    # button_data = query.data.split(" ")
    # # Ignore if the query data unexpected or comes from an unexpected user
    # if (len(button_data) < 2) or (button_data[1] != str(query.from_user.id)):
    #     return



def msg_new_user(update, context):
    update_msg = getattr(update, "message", None)
    UserId = update_msg.User.id
    global to_delete_join_messages_list
    global new_users_list
    bot = context.bot
    #bot = context.bot

    #reply_markup = InlineKeyboardMarkup(keyboard)
    for join_user in update_msg.new_chat_members:
        #join_user_id = join_user.id
        # Get user name
        if join_user.name is not None:
            join_user_name = join_user.name
        else:
            join_user_name = join_user.full_name
        # Add an unicode Left to Right Mark (LRM) to user name (names fix for arabic, hebrew, etc.)
        join_user_name = add_lrm(join_user_name)
        # If the user name is too long, truncate it to 35 characters
        if len(join_user_name) > 35:
            join_user_name = join_user_name[0:35]
    bot.send_message(UserId, f'Hi, {join_user_name}. Welcome to the MakeLab Israel telegram group! Please answer the question by typing the answer in the chat:')
    #update.message.reply_text(f'Hi, {join_user_name}. Please answer the question by typing the answer in the chat:')
    return REPLY
    #update_new_users = getattr(update,  new_users_list)
#    print(update_new_users)
    #update.message.new_chat_members


#def starting(update, context):
    #update.message.reply_text(f'Hi, {join_user_name}. Please answer the question by typing the answer in the chat:')
    #return GREET


def echo(update, context):
    """Echo the user message."""
    bot = context.bot
    update_chat_id = getattr(update, "message", None)
    memberid1 = update_chat_id.from_user
    memberid = memberid1.id
    

    chatid = update_chat_id.chat_id

    message = update.message.text
    permis = ChatPermissions(False, False, False, False, False, False, False, False)
    bot.restrict_chat_member(chatid, memberid, permis)
    admins = bot.getChatAdministrators(chatid)
    
    #context.user_data['id'] = chatid
    #bot.send_message('1050861060', message)
    for admin in admins:
        tempadmin = admin.user
        tempadmin2 = tempadmin.id
        print(tempadmin2)
        if tempadmin.is_bot == False :
            bot.send_message(tempadmin2, message)
            bot.send_message(tempadmin2, 'Reply /verify to verify or /kick to kick user')
    return ConversationHandler.END
        
        #bot.send_message(tempadmin2, message)

# def verify(update, context):
#     bot = context.bot
#     permiss = ChatPermissions(True, True, True, True, True, True, True, True)
#     bot.restrict_chat_member(normalchatid, resuserid, permiss)

# def kick(update, context):
#     bot = context.bot
#     bot.kick_chat_member(normalchatid, resuserid)



        

def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater("1178519912:AAFYhejGRdrIySmbB1w-AOAQ5y3YBmoBiqg", use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    #dp.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))
    
    #dp.add_handler(MessageHandler(Filters.status_update.new_chat_members, msg_new_user))
    conv_handler = ConversationHandler(entry_points=[MessageHandler(Filters.status_update.new_chat_members, msg_new_user)],

        states={
            REPLY: [
                MessageHandler(Filters.text, echo)],
        },

        fallbacks=[CommandHandler('stop', msg_new_user)]
    )

    dp.add_handler(conv_handler)
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help_command))
    # dp.add_handler(CommandHandler("verify", verify))
    # dp.add_handler(CommandHandler("kick", kick))
   # , filters=(Filter.chat('1050861060')
    # on noncommand i.e message - echo the message on Telegram

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()