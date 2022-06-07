""" This python file contains the code for calling the telegram notifier class """

import sys
import os

from notifications.telegram_notifier import TelegramNotifier

if __name__ == '__main__':
    bot_token = os.environ['TELEGRAM_BOT_TOKEN']
    chat_id = os.environ['TELEGRAM_CHAT_ID']

    if bot_token is None or chat_id is None:
        print(
            "Please set the TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID environment variables")
        sys.exit(1)
    telegram_notifier = TelegramNotifier(bot_token, chat_id)

    if len(sys.argv) < 2:
        print(f'Usage: {sys.argv[0]} <message_type>')
        sys.exit(1)

    message_type = sys.argv[1]
    if message_type == 'pr_opened':
        if len(sys.argv) != 5:
            print(
                f'Usage: {sys.argv[0]} pr_opened <pr_author> <pr_title> <pr_url>'
            )
            sys.exit(1)
        pr_author = sys.argv[2]
        pr_title = sys.argv[3]
        pr_url = sys.argv[4]
        telegram_notifier.notify_pr_opened(pr_author, pr_title, pr_url)
    elif message_type == 'low_precision':
        if len(sys.argv) != 6:
            print(
                f"Usage: {sys.argv[0]} low_precision <pr_author> <pr_title>" +
                " <pr_url> <model_precision>"
            )
            sys.exit(1)
        [_, _, pr_author, pr_title, pr_url, model_precision] = sys.argv
        telegram_notifier.notify_low_precision(
            pr_author, pr_title, pr_url, model_precision)
