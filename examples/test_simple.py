from telebot import TeleBot
from telebot_tests import BaseBotTestCase

bot = TeleBot('abc:123')

@bot.message_handler(commands=['start'])
def start(msg):
    sent = bot.send_message(
        chat_id=msg.chat.id,
        text="Hello, World!",
    )

class MyBotTestCase(BaseBotTestCase):
    bot=bot

    def setUp(self):
        super().setUp()
        self.tg_faker.response_value(method='sendMessage', result=self.tg_faker.send_message_response())

    def test_ok(self):
        self.receive_message(message_id=1, text='/start')

        self.process_updates()

        self.assertEqual(len(self.tg_faker.requests), 1)
        self.assertEqual(
            self.tg_faker.requests[0].params,
            dict(
                chat_id='1',
                text='Hello, World!',
            ),
        )
