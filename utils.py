import os

LOG_FILE = "bot_logs.txt"

def log_usage(message, bot=None):
    """Logs bot usage to a file and sends it to the logs group."""
    with open(LOG_FILE, "a") as log_file:
        log_file.write(message + "\n")

    if bot:
        from config import LOGS_GROUP_ID
        bot.send_message(chat_id=LOGS_GROUP_ID, text=message)

def count_users(users):
    """Returns the number of unique users using the bot."""
    return len(users)
