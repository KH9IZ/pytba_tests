# -*- coding: utf-8 -*-
import json
from pytba_tests import BaseBotTestCase

from your_project import bot


class CreateCounterTestCase(BaseBotTestCase):
    bot = bot

    def setUp(self):
        super().setUp()
        self.tg_faker.response_value(method='deleteMessage', result=self.tg_bot.delete_message_response())
        self.tg_faker.response_value(method='sendMessage', result=self.tg_bot.send_message_response())

    def test_ok(self):
        self.receive_message(message_id=1, text='/start')

        self.process_updates()

        self.assertEqual(len(self.tg_faker.requests), 2)
        self.assertEqual(self.tg_faker.requests[0].params, dict(chat_id=1, message_id=1))
        self.assertEqual(
            self.tg_faker.requests[1].params,
            dict(
                chat_id='1',
                parse_mode='markdown',
                reply_markup=json.dumps(dict(
                    inline_keyboard=[
                        [
                            dict(text="-1", callback_data='-1'),
                            dict(text="+1", callback_data='+1'),
                        ],
                    ],
                )),
                text='{counter_name} {cnt}'.format(counter_name='', cnt=0),
            ),
        )

    def test_ok_create(self):
        self.receive_message(message_id=1, text='/create')

        self.process_updates()

        self.assertEqual(len(self.tg_faker.requests), 2)
        self.assertEqual(self.tg_faker.requests[0].params, dict(chat_id=1, message_id=1))
