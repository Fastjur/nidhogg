import sys
import os

from TelegramNotifier import TelegramNotifier

if __name__ == '__main__':
    bot_token = os.environ['TELEGRAM_BOT_TOKEN']
    chat_id = os.environ['TELEGRAM_CHAT_ID']

    if bot_token is None or chat_id is None:
        print("Please set the TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID environment variables")
        sys.exit(1)
    telegram_notifier = TelegramNotifier(bot_token, chat_id)

    if len(sys.argv) < 2:
        print('Usage: {} <message_type>'.format(sys.argv[0]))
        sys.exit(1)

    message_type = sys.argv[1]
    if message_type == 'pr_opened':
        if len(sys.argv) != 5:
            print('Usage: {} pr_opened <pr_author> <pr_title> <pr_url>'.format(sys.argv[0]))
            sys.exit(1)
        pr_author = sys.argv[2]
        pr_title = sys.argv[3]
        pr_url = sys.argv[4]
        telegram_notifier.notify_pr_opened(pr_author, pr_title, pr_url)