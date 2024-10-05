from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler, CallbackContext
from video import compress_video
from config import BOT_TOKEN, OWNER_ID
from utils import log_usage, count_users
import time
from collections import deque

users = set()
video_queue = deque()  # Queue to manage video compression requests

def start(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    username = update.effective_user.username
    users.add(user_id)

    image_url = "https://i.imghippo.com/files/hm6zJ1727977742.jpg"

    caption1 = (
        "𝖧𝖾𝗅𝗅𝗈 𝗍𝗁𝖾𝗋𝖾!\n"
        "𝖶𝖾𝗅𝖼𝗈m𝖾 𝗍𝗈 𝗔𝗹𝗰𝘆𝗼𝗻𝗲 𝗩𝗶𝗱𝗲𝗼 𝗖𝗼𝗺𝗽𝗿𝗲𝘀𝘀𝗼𝗿 Bot!\n"
        "𝖸𝗈𝗎𝗋 𝗀𝗈-𝗍𝗈 𝗍𝗈𝗈𝗹 𝖿𝗈𝗋 𝖼𝗈𝗆𝗉𝗋𝖾𝗌𝗌𝗂𝗇𝗀 𝗏𝗂𝖽𝖾𝗈𝗌 𝗐𝗂𝗍𝗁𝗈𝗎𝗍 𝗅𝗈𝗌𝗂𝗇𝗀 𝗊𝗎𝖺𝗅𝗂𝗍𝗒! 🎬\n"
        "➥ J𝗎𝗌𝗍 𝗌𝖾𝗇𝖽 m𝖾 𝖺 𝗏𝗂𝖽𝖾𝗈 𝖿𝗂𝗅𝖾 𝖺nd I'𝗅𝗅 𝗍𝖺𝗄𝖾 𝖼𝖺𝗋𝖾 𝗈𝖿 𝗍𝗁𝖾 𝖼𝗈𝗆𝗉𝗋𝖾𝗌𝗌𝗂𝗈𝗇!\n"
    )

    caption2 = (
        "ⓘ 𝖬𝖺k𝖾 sure to 𝗌𝗎b𝗌𝖼𝗋𝗂𝖻𝖾𝖽 𝗍𝗈 𝗈𝗎𝗋 𝗈𝖋𝖿𝗂𝖼𝗂𝖺𝗅 𝖼𝗁𝖺𝗇𝗇𝖾𝗅 𝖺n𝖽 𝗌𝗎𝗉𝗉𝗈r𝗍 𝖼𝗁𝖺𝗍 𝗍𝗈 𝗀𝖾𝗍 𝗍𝗁𝖾 𝖻𝖾𝗌𝗍 𝖾𝗑pe𝗋𝗂𝖾𝗇c𝖾!\n\n"
        "👾 𝖫𝖾𝗍𝗌 𝖣𝗂𝗏𝖾 𝗂𝗇 𝖼𝗈𝗆𝗉𝗋𝖾𝗌𝗌 𝗍𝗁𝗈𝗌𝖾 𝗏𝗂𝖽e𝗈𝗌!!"
    )

    # Send the image with the first part of the caption
    context.bot.send_photo(chat_id=update.effective_chat.id, photo=image_url, caption=caption1)

    # Create inline buttons
    keyboard = [
        [
            InlineKeyboardButton("𝖡𝗈𝗍 𝖴𝗉𝖽𝖺𝗍𝖾𝗌", url="https://t.me/AlcyoneBots"),
            InlineKeyboardButton("𝖡𝗈𝗍 𝖲𝗎𝗉𝗉𝗈𝗋𝗍", url="https://t.me/Alcyone_Support"),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Send the second part of the caption with inline buttons
    context.bot.send_message(chat_id=update.effective_chat.id, text=caption2, reply_markup=reply_markup)

    log_usage(f"𝖴𝗌𝖾𝗋 {username} \nID: {user_id} 𝗌𝗍𝖺𝗋𝗍𝖾𝖽 𝗍𝗁𝖾 𝖻𝗈𝗍", context.bot)

def ping(update: Update, context: CallbackContext):
    start_time = time.time() 
    update.message.reply_text("🏓 𝖯𝗈𝗇𝗀!")
    end_time = time.time() 
    response_time = (end_time - start_time) * 1000 
    update.message.reply_text(f"𝖱𝖾𝗌𝗉𝗈𝗇s𝖾 𝖻𝖾𝖺𝗋𝗂𝗇𝗀 𝖳𝗂𝗆𝖾: {int(response_time)} ms")

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
        video_queue.append((user_id, video_path))  # Add video to the queue
        log_usage(f"𝖴𝗌𝖾𝗋 {username}\n𝖴𝗌𝖾𝗋𝖨𝖣: {user_id}\n𝖲𝖾𝗇𝗍 𝖺 𝗏𝗂𝖽𝖾𝗈 𝖿𝗈𝗋 𝖼𝗈𝗆𝗉𝗋𝖾𝗌𝗌𝗂𝗈𝗇 👾", context.bot)

        # Start processing if not already in progress
        if not context.user_data.get('compression_in_progress', False):
            handle_compression(context)

def handle_compression(context: CallbackContext):
    if video_queue:
        context.user_data['compression_in_progress'] = True  # Set flag to indicate compression is in progress
        user_id, video_path = video_queue.popleft()  # Get the next video to process

        # Ask user to choose compression type
        context.bot.send_message(chat_id=user_id, text="🔧 𝖢𝗁𝗈𝗌𝖾 𝖼𝗈m𝗉𝗋𝖾𝗌𝗌𝗂𝗈𝗇 𝗍𝗒𝗉𝖾:", reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("𝖥𝖺𝗌𝗍 𝖢𝗈𝗆𝗉𝗋𝖾𝗌𝗌𝗂𝗈𝗇", callback_data='fast')],
            [InlineKeyboardButton("𝖧𝗂𝗀𝗁 𝖰𝗎𝖺𝗅𝗂𝗍𝗒 𝖢𝗈𝗆𝗉𝗋𝖾𝗌𝗌𝗂𝗈𝗇", callback_data='hq')]
        ]))

def handle_query(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    
    user_id = query.from_user.id
    username = query.from_user.username

    if query.data == 'fast':
        query.edit_message_text(text="𝖢𝗈𝗆𝗉𝗋𝖾𝗌𝗌𝗂𝗇𝗀 𝗏𝗂𝖽e𝗈 𝗐𝗂𝗍𝗁 𝖿𝖺𝗌𝗍 𝗌𝖾𝗍𝗍𝗂𝗇𝗀𝗌...")
        compressed_video_path = compress_video(query.message.reply_to_message.video.file_id, fast=True)
        context.bot.send_video(chat_id=user_id, video=open(compressed_video_path, 'rb'), caption=" ")
    elif query.data == 'hq':
        query.edit_message_text(text="𝖢𝗈𝗆𝗉𝗋𝖾𝗌𝗌𝗌𝗂𝗇𝗀 𝗏𝗂𝖽e𝗈 𝗐𝗂𝗍𝗁 𝗁𝗂𝗀𝗁 𝖰𝗎𝖺𝗇𝗍𝗂𝗍𝗒...")
        compressed_video_path = compress_video(query.message.reply_to_message.video.file_id, fast=False)
        context.bot.send_video(chat_id=user_id, video=open(compressed_video_path, 'rb'), caption=" ")

    # Remove video from the queue and continue processing if there are more videos
    if video_queue:
        handle_compression(context)
    else:
        context.user_data['compression_in_progress'] = False  # Reset flag if no more videos
        

def broadcast(update: Update, context: CallbackContext):
    if update.effective_user.id == OWNER_ID:
        if context.args:
            message = ' '.join(context.args)
            for user in users:
                context.bot.send_message(chat_id=user, text=message)
            update.message.reply_text(" Broadcast for all users completed successfully!!")
        else:
            update.message.reply_text("𝖯𝗅𝖾𝖺𝗌𝖾 𝗌𝖾𝗇𝖽 𝖺 m𝖾𝗌𝖺𝗀𝖾!")
    else:
        update.message.reply_text("Only Owner can use this command")

def help_command(update: Update, context: CallbackContext):
    help_text = (
        "The following Commands are available for the Bot \n"
        "➜ /start - To start the bot \n"
        "➜ /status - To check the ongoing status of the compression \n"
        "➜ /broadcast <message> - Broadcast a message to the users (Owner Command) \n"
        "➜ /compress - 𝖢𝗁𝗈𝗌𝖾 𝖼𝗈𝗆𝗉𝗋𝖾𝗌𝗌𝗂𝗈𝗇 type \n"
        "➜ /help - To show all commands \n"
    )
    update.message.reply_text(help_text)

def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("ping", ping))
    dp.add_handler(CommandHandler("compress", compress))
    dp.add_handler(CommandHandler("broadcast", broadcast))
    dp.add_handler(CommandHandler("help", help_command))
    dp.add_handler(MessageHandler(Filters.video, handle_video))
    dp.add_handler(CallbackQueryHandler(handle_query))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
