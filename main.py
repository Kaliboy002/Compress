from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler, CallbackContext
from video import compress_video
from config import BOT_TOKEN, OWNER_ID
from utils import log_usage, count_users
import time

users = set()  # Keep track of users who have interacted with the bot

def start(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    username = update.effective_user.username
    users.add(user_id)  # Track users
    
    # Inline buttons for updates and support
    keyboard = [
        [InlineKeyboardButton("Bot Updates", url="https://t.me/alcyonebots")],
        [InlineKeyboardButton("Bot Support", url="https://t.me/alcyone_support")]
    ]
    
    update.message.reply_text(
        "Welcome to Alcyone Video Compressor Bot! Choose an option:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )
    
    # Send logs to the logs group
    log_usage(f"User {username} (ID: {user_id}) started the bot.", context.bot)

def ping(update: Update, context: CallbackContext):
    start_time = time.time()  # Record start time
    update.message.reply_text("🏓 Pong!")
    end_time = time.time()  # Record end time
    response_time = (end_time - start_time) * 1000  # Calculate response time in ms
    update.message.reply_text(f"Response time: {int(response_time)} ms")

def compress(update: Update, context: CallbackContext):
    # Show inline buttons for compression options
    update.message.reply_text("Choose compression quality:",
                              reply_markup=InlineKeyboardMarkup([
                                  [InlineKeyboardButton("Fast Compression", callback_data='fast')],
                                  [InlineKeyboardButton("High Quality Compression", callback_data='hq')],
                              ]))

def handle_video(update: Update, context: CallbackContext):
    video_file = update.message.video
    user_id = update.effective_user.id
    username = update.effective_user.username

    if video_file:
        video_path = video_file.get_file().download()

        # Show compression options
        compress(update, context)

        # Log the video upload event
        log_usage(f"User {username} (ID: {user_id}) sent a video for compression.", context.bot)

def handle_query(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    
    user_id = query.from_user.id
    username = query.from_user.username

    if query.data == 'fast':
        query.edit_message_text(text="Compressing video with fast settings...")
        compressed_video = compress_video(query.message, fast=True)
        log_usage(f"User {username} (ID: {user_id}) chose fast compression.", context.bot)
    elif query.data == 'hq':
        query.edit_message_text(text="Compressing video with high quality settings...")
        compressed_video = compress_video(query.message, fast=False)
        log_usage(f"User {username} (ID: {user_id}) chose high quality compression.", context.bot)
    
    # Send the compressed video back to the user
    context.bot.send_video(chat_id=query.message.chat.id, video=open(compressed_video, 'rb'))

    # Update log with user count
    log_usage(f"Total users using the bot: {count_users(users)}", context.bot)

def broadcast(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    if user_id == OWNER_ID:
        message = " ".join(context.args)
        if not message:
            update.message.reply_text("Please provide a message to broadcast.")
            return

        for user in users:
            try:
                context.bot.send_message(chat_id=user, text=message)
            except Exception as e:
                log_usage(f"Failed to send message to {user}: {e}", context.bot)
        
        update.message.reply_text("Message broadcasted.")
    else:
        update.message.reply_text("You are not authorized to use this command.")

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
