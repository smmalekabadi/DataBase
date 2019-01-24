# from telegram.ext import Updater, CommandHandler
# import telegram.bot
#
#
# def hello(bot, update):
#     print("bot")
#     update.message.reply_text(
#         'Hello {}'.format(update.message.from_user.first_name))
#
# def start(bot, update):
#     bot.send_message(chat_id=update.message.chat_id, text="I'm a bot, please talk to me!")
#
# updater = Updater('515599702:AAG3Vs50RhpiIn07dtNJWTrCRsHj83CvYsI')
#
# dispatcher = updater.dispatcher
#
# updater.dispatcher.add_handler(CommandHandler('hello', hello))
#
# updater.start_polling()
# updater.idle()


# bot = telegram.Bot(token="515599702:AAG3Vs50RhpiIn07dtNJWTrCRsHj83CvYsI")
#                         # 651293792:AAH1CHHI6B_CbcxcR1O8KokIfffPCK6DfCI
# print(bot.get_me())
#
#

import telepot
tok = '515599702:AAG3Vs50RhpiIn07dtNJWTrCRsHj83CvYsI'

bot = telepot.Bot('515599702:AAG3Vs50RhpiIn07dtNJWTrCRsHj83CvYsI')
bot.getMe()