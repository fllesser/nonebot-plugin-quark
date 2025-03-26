from nonebot.log import logger
import pytest


@pytest.mark.asyncio
async def test_search():
    from nonebot_plugin_quark.data_source import search

    result = await search("花园宝宝")
    for info in result:
        logger.info(info)
