from nonebot.adapters.onebot.v11 import Bot, GroupMessageEvent, Message  # noqa: F401
from nonebug import App
import pytest


def make_onebot_msg(message: Message) -> GroupMessageEvent:
    from time import time

    from nonebot.adapters.onebot.v11.event import Sender

    event = GroupMessageEvent(
        time=int(time()),
        sub_type="normal",
        self_id=123456,
        post_type="message",
        message_type="group",
        message_id=12345623,
        user_id=1234567890,
        group_id=1234567890,
        raw_message=message.extract_plain_text(),
        message=message,
        original_message=message,
        sender=Sender(),
        font=123456,
    )
    return event


@pytest.mark.asyncio
async def test_load(app: App):
    from nonebot import require

    assert require("nonebot_plugin_quark")


@pytest.mark.asyncio
async def test_quark_so():
    pass
