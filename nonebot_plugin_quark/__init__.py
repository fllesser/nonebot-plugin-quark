import asyncio

from nonebot.plugin import on_command
from nonebot.params import CommandArg
from nonebot.adapters.onebot.v11 import (
    Bot,
    MessageSegment,
    Message,
    MessageEvent,
    PRIVATE
)

from .data_source import search

quark = on_command(cmd='qs', block=True)

@quark.handle()
async def _(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
    keyword = args.extract_plain_text().strip()
    if not keyword:
        return
    if url_info_list := await search(keyword):
        format_info_list = [str(info) for info in url_info_list]
        res = construct_nodes(bot.self_id, format_info_list) 
    else:
        res = "未搜索到相关资源"
    await quark.finish(res)
    

def construct_nodes(user_id: int, segments: MessageSegment | list) -> Message:
    def node(content):
        return MessageSegment.node_custom(user_id=user_id, nickname='quark search', content=content)
    segments = segments if isinstance(segments, list) else [segments]
    return Message([node(seg) for seg in segments])
