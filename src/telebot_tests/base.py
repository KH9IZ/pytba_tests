from unittest import TestCase

from telebot.types import (
    Update,
)
from telebot import (
    apihelper,
    TeleBot,
)
from .tg_faker import TgFaker
from .utils import (
    build_callback_query,
    build_message,
    build_update,
)


class BaseBotTestCase(TestCase):
    """Base class for all TestCases. Incapsulate many helpful functions and tg_faker."""
    __updates: list[Update]  # List of updates to process
    __id_counter: int  # Counter for updates
    bot: TeleBot | None = None

    def setUp(self):
        if self.bot is None:
            raise AttributeError("bot attribute needed")

        super().setUp()

        self.__updates = []
        self.__id_counter = 0
        self.tg_faker = TgFaker()  # object mocking tg_api responses
        self.bot.threaded = False
        apihelper.CUSTOM_REQUEST_SENDER = self.tg_faker.request_sender

    def generate_id(self):
        self.__id_counter += 1
        return self.__id_counter

    def receive_message(
        self,
        message_id=None,
        content_type=None,
        text=None,
        reply_to=None,
        dice=None,
    ):
        """Emulate single message update from user to bot."""
        self.receive_update(message=build_message(
            message_id=message_id or self.generate_id(),
            text=text,
            reply_to=reply_to,
            content_type=content_type,
            dice=dice,
        ))

    def receive_callback_query(self, callback_id=None, data=None, message=None):
        """Emulate single callback query from user to bot."""
        self.receive_update(callback_query=build_callback_query(
            callback_id=callback_id or self.generate_id(),
            data=data,
            message=message,
        ))

    def receive_update(self, message=None, callback_query=None):
        """Emulate single message update from user to bot."""
        if not any((message, callback_query)):
            raise ValueError("Unsupported update type")

        self.__updates.append(build_update(
            update_id=self.generate_id(),
            message=message,
            callback_query=callback_query,
        ))

    def process_updates(self, extra_updates: list[Update] = None):
        """
        Make bot process received updates.
        >>> def test_ok(self):
        >>>     self.receive_message(text='/start')
        >>>     self.process_updates()
        """
        if extra_updates:
            self.__updates.extend(extra_updates)

        self.bot.process_new_updates(self.__updates)
        self.__updates = []
