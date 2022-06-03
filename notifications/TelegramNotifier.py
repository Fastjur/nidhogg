import sys

import requests


class TelegramNotifier:
    def __init__(self, bot_token, chat_id):
        self.bot_token = bot_token
        self.chat_id = chat_id

    def notify(self, message, inline_keyboard_markup):
        url = 'https://api.telegram.org/bot{}/sendMessage'.format(self.bot_token)
        data = {
            'chat_id': self.chat_id,
            'text': message,
            'parse_mode': 'Markdown',
            'reply_markup': {
                'inline_keyboard': inline_keyboard_markup
            },
        }
        print(data)
        res = requests.post(url, json=data)
        if res.status_code < 200 or res.status_code >= 300:
            print("❌ Error sending message:")
            print(res.text)
            sys.exit(1)

    def notify_pr_opened(self, pr_author, pr_title, pr_url):
        with open('templates/pr_opened.txt') as f:
            message_text = ''.join(f.readlines()).format(pr_author, pr_title, pr_url)
            print("📩 Sending message:")
            print(message_text)

            inline_keyboard_markup = [
                    [{'text': 'View on GitHub', 'url': pr_url}]
            ]
            self.notify(message_text, inline_keyboard_markup)
