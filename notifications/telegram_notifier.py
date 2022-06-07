""" This file contains the telegram notifier class """

import sys

import requests


class TelegramNotifier:
    """ This class wraps some of the telegram api methods """

    def __init__(self, bot_token, chat_id):
        self.bot_token = bot_token
        self.chat_id = chat_id

    def notify(self, message, inline_keyboard_markup):
        """ Send a message to the telegram chat """
        url = f'https://api.telegram.org/bot{self.bot_token}/sendMessage'
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
        """ Create the relevance buttons for the given message type """
        default_buttons = [
            {
                'text': 'Relevant',
                'url': f'http://127.0.0.1:3001/vote?category={"PR"}&id={message_type}&vote=positive'
            },
            {
                'text': 'Irrelevant',
                'url': f'http://127.0.0.1:3001/vote?category={"PR"}&id={message_type}&vote=negative'
            },
       ]
        if message_type in ('pr_opened', 'low_precision'):
            return default_buttons
        raise Exception(f'Unknown message type: {message_type}')

    def notify_pr_opened(self, pr_author, pr_title, pr_url):
        """ Send a message when a PR is opened """
        with open('templates/pr_opened.txt', encoding="utf-8") as template_file:
            message_type = 'pr_opened'
            message_text = ''.join(
                template_file.readlines()).format(
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

    def notify_low_precision(
            self,
            pr_author,
            pr_title,
            pr_url,
            model_precision
    ):
        """ Send a message when a PR is opened with low precision """
        with open('templates/low_precision.txt', encoding="utf-8") as template_file:
            message_type = 'low_precision'
            message_text = ''.join(
                template_file.readlines()).format(
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
