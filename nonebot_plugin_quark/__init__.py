from nonebot import on_command, require  # noqa: F401
from nonebot.plugin import PluginMetadata, inherit_supported_adapters

require("nonebot_plugin_alconna")

from .data_source import search

__plugin_meta__ = PluginMetadata(
    name="夸克搜",
    description="NoneBot2 夸克资源搜索插件",
    usage="qs 关键词",
    type="application",
    homepage="https://github.com/fllesser/nonebot-plugin-quark",
    supported_adapters=inherit_supported_adapters("nonebot_plugin_alconna"),
    extra={"author": "fllesser <fllessive@gmail.com>"},
)

from arclet.alconna import Alconna, Args
from nonebot_plugin_alconna import Match, on_alconna
from nonebot_plugin_alconna.uniseg import Text, UniMessage

alc = Alconna(
    "qs",
    Args["keyword", str],
)


@on_alconna(alc).handle()
async def _(keyword: Match[str]):
    if not keyword.available:
        return
    kwd: str = keyword.result

    receipt = await UniMessage.text("搜索资源中...").send()
    try:
        url_info_lst = await search(kwd)
    except Exception as e:
        await UniMessage.text(f"搜索出错: {e}").send()
        raise
    finally:
        await receipt.recall()

    if not url_info_lst:
        await UniMessage.text("未搜索到相关资源，请稍后再试").finish()
    text_lst = [Text(str(info)) for info in url_info_lst]
    await UniMessage(text_lst).send()


# def construct_nodes(user_id: int, segments: MessageSegment | list) -> Message:
#     def node(content):
#         return MessageSegment.node_custom(user_id=user_id, nickname="Quark", content=content)

#     segments = segments if isinstance(segments, list) else [segments]
#     return Message([node(seg) for seg in segments])
