from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler, CallbackContext
from video import compress_video
from config import BOT_TOKEN, OWNER_ID
from utils import log_usage, count_users
import time

users = set()

def start(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    username = update.effective_user.username
    users.add(user_id)  
    
    keyboard = [
        [InlineKeyboardButton("𝖡𝗈𝗍 𝖴𝗉𝖽𝖺𝗍𝖾𝗌", url="https://t.me/alcyonebots")],
        [InlineKeyboardButton("𝖡𝗈𝗍 𝖲𝗎𝗉𝗉𝗈𝗋𝗍", url="https://t.me/alcyone_support")]
    ]
    
    update.message.reply_text(
        "Welcome to Alcyone Video Compressor Bot! Choose an option:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )
    
    log_usage(f"User {username} (ID: {user_id}) started the bot.", context.bot)

def ping(update: Update, context: CallbackContext):
    start_time = time.time() 
    update.message.reply_text("🏓 𝖯𝗈𝗇𝗀!")
    end_time = time.time() 
    response_time = (end_time - start_time) * 1000 
    update.message.reply_text(f"Response time: {int(response_time)} ms")

def compress(update: Update, context: CallbackContext):
    update.message.reply_text("𝖢𝗁𝗈𝗈𝗌𝖾 𝖼𝗈𝗆𝗉𝗋𝖾𝗌𝗌𝗂𝗈𝗇 𝗊𝗎𝖺𝗅𝗂𝗍𝗒:",
                              reply_markup=InlineKeyboardMarkup([
                                  [InlineKeyboardButton("𝖥𝖺𝗌𝗍 𝖢𝗈𝗆𝗉𝗋𝖾𝗌𝗌𝗂𝗈𝗇", callback_data='fast')],
                                  [InlineKeyboardButton("𝖧𝗂𝗀𝗁 𝖰𝗎𝖺𝗅𝗂𝗍𝗒 𝖢𝗈𝗆𝗉𝗋𝖾𝗌𝗌𝗂𝗈𝗇", callback_data='hq')],
                              ]))

def handle_video(update: Update, context: CallbackContext):
    video_file = update.message.video
    user_id = update.effective_user.id
    username = update.effective_user.username

    if video_file:
        video_path = video_file.get_file().download()

        compress(update, context)

        log_usage(f"𝖴𝗌𝖾𝗋 {username}\n 𝖴𝗌𝖾𝗋𝖨𝖣: {user_id}\n𝖲𝖾𝗇𝗍 𝖺 𝗏𝗂𝖽𝖾𝗈 𝖿𝗈𝗋 𝖼𝗈𝗆𝗉𝗋𝖾𝗌𝗌𝗂𝗈𝗇 👾", context.bot)

def handle_query(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    
    user_id = query.from_user.id
    username = query.from_user.username

    if query.data == 'fast':
        query.edit_message_text(text="𝖢𝗈𝗆𝗉𝗋𝖾𝗌𝗌𝗂𝗇𝗀 𝗏𝗂𝖽𝖾𝗈 𝗐𝗂𝗍𝗁 𝖿𝖺𝗌𝗍 𝗌𝖾𝗍𝗍𝗂𝗇𝗀𝗌...")
        compressed_video = compress_video(query.message, fast=True)
        log_usage(f"𝖴𝗌𝖾𝗋 {username} \n𝖴𝗌𝖾𝗋𝖨𝖣: {user_id} \n𝖢𝗁𝗈𝗌𝖾 𝖿𝖺𝗌𝗍 𝖼𝗈𝗆𝗉𝗋𝖾𝗌𝗌𝗂𝗈𝗇.", context.bot)
    elif query.data == 'hq':
        query.edit_message_text(text="𝖢𝗈𝗆𝗉𝗋𝖾𝗌𝗌𝗂𝗇𝗀 𝗏𝗂𝖽𝖾𝗈 𝗐𝗂𝗍𝗁 𝗁𝗂𝗀𝗁 𝗊𝗎𝖺𝗅𝗂𝗍𝗒 𝗌𝖾𝗍𝗍𝗂𝗇𝗀𝗌...")
        compressed_video = compress_video(query.message, fast=False)
        log_usage(f"𝖴𝗌𝖾𝗋 {username}\n𝖴𝗌𝖾𝗋𝖨𝖣: {user_id} 𝖢𝗁𝗈𝗌𝖾 𝗁𝗂𝗀𝗁 𝗊𝗎𝖺𝗅𝗂𝗍𝗒 𝖼𝗈𝗆𝗉𝗋𝖾𝗌𝗌𝗂𝗈𝗇.", context.bot)
    
    context.bot.send_video(chat_id=query.message.chat.id, video=open(compressed_video, 'rb'))
    
    log_usage(f"𝖳𝗈𝗍𝖺𝗅 𝗎𝗌𝖾𝗋𝗌 𝗎𝗌𝗂𝗇𝗀 𝗍𝗁𝖾 𝖻𝗈𝗍: {count_users(users)}", context.bot)

def broadcast(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    if user_id == OWNER_ID:
        message = " ".join(context.args)
        if not message:
            update.message.reply_text("𝖯𝗅𝖾𝖺𝗌𝖾 𝗉𝗋𝗈𝗏𝗂𝖽𝖾 𝖺 𝗆𝖾𝗌𝗌𝖺𝗀𝖾 𝗍𝗈 𝖻𝗋𝗈𝖺𝖽𝖼𝖺𝗌𝗍.")
            return

        for user in users:
            try:
                context.bot.send_message(chat_id=user, text=message)
            except Exception as e:
                log_usage(f"𝖥𝖺𝗂𝗅𝖾𝖽 𝗍𝗈 𝗌𝖾𝗇𝖽 𝗆𝖾𝗌𝗌𝖺𝗀𝖾 𝗍𝗈 {user}: {e}", context.bot)
        
        update.message.reply_text("𝖬𝖾𝗌𝗌𝖺𝗀𝖾 𝖻𝗋𝗈𝖺𝖽𝖼𝖺𝗌𝗍𝖾𝖽.")
    else:
        update.message.reply_text("𝖮𝗇𝗅𝗒 𝖮𝗐𝗇𝖾𝗋 𝖼𝖺𝗇 𝗎𝗌𝖾 𝗍𝗁𝗂𝗌 𝖼𝗈𝗆𝗆𝖺𝗇𝖽!!")

def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('ping', ping))
    dp.add_handler(CommandHandler('compress', compress))
    dp.add_handler(CommandHandler('broadcast', broadcast))
    dp.add_handler(MessageHandler(Filters.video, handle_video))
    dp.add_handler(CallbackQueryHandler(handle_query))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
