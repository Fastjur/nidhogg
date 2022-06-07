import sys

import requests


class TelegramNotifier:
    def __init__(self, bot_token, chat_id):
        self.bot_token = bot_token
        self.chat_id = chat_id

    def notify(self, message, inline_keyboard_markup):
        url = 'https://api.telegram.org/bot{}/sendMessage'.format(
            self.bot_token)
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

    @staticmethod
    def create_relevance_buttons(message_type):
        default_buttons = [{'text': 'Relevant',
                            'url': 'http://127.0.0.1:3001/vote?category={}&id={}&vote=positive'.format('PR',
                                                                                                       message_type)},
                           {'text': 'Irrelevant',
                            'url': 'http://127.0.0.1:3001/vote?category={}&id={}&vote=negative'.format('PR',
                                                                                                       message_type)},
                           ]
        if message_type == 'pr_opened' or message_type == 'low_precision':
            return default_buttons
        raise Exception('Unknown message type: {}'.format(message_type))

    def notify_pr_opened(self, pr_author, pr_title, pr_url):
        with open('templates/pr_opened.txt') as f:
            message_type = 'pr_opened'
            message_text = ''.join(
                f.readlines()).format(
                pr_author,
                pr_title,
                pr_url,
                message_type)
            print("📩 Sending message:")
            print(message_text)

            inline_keyboard_markup = [
                [{'text': 'View on GitHub', 'url': pr_url}],
                self.create_relevance_buttons(message_type)
            ]
            self.notify(message_text, inline_keyboard_markup)

    def notify_low_precision(self, pr_author, pr_title,
                             pr_url, model_precision):
        with open('templates/low_precision.txt') as f:
            message_type = 'low_precision'
            message_text = ''.join(
                f.readlines()).format(
                model_precision,
                pr_author,
                pr_title,
                pr_url,
                message_type)
            print("📩 Sending message:")
            print(message_text)

            inline_keyboard_markup = [
                [{'text': 'View on GitHub', 'url': pr_url}],
                self.create_relevance_buttons(message_type)
            ]
            self.notify(message_text, inline_keyboard_markup)
