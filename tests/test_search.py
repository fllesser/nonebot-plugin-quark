from nonebot.log import logger
import pytest


@pytest.mark.asyncio
async def test_search():
    import time

    from nonebot_plugin_quark.data_source import search

    start_time = time.time()
    result = await search("剑来")
    end_time = time.time()
    logger.info(f"搜索时间: {end_time - start_time} 秒")
    for info in result:
        logger.info(info)
