import asyncio

from nonebot.plugin import on_command
from nonebot.params import CommandArg
from nonebot.adapters.onebot.v11 import (
    Bot,
    Message,
    MessageEvent,
    MessageSegment
)

from nonebot.plugin import PluginMetadata

from .data_source import search


__plugin_meta__ = PluginMetadata(
    name="夸克搜",
    description="NoneBot2 夸克资源搜索插件",
    usage="qs 关键词",
    type="application",
    homepage="https://github.com/fllesser/nonebot-plugin-quark",
    supported_adapters={ "~onebot.v11" }
)


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
