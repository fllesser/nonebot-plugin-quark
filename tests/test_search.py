from nonebot.log import logger
import pytest


@pytest.mark.asyncio
async def test_search():
    import time

    from nonebot_plugin_quark.data_source import search

    start_time = time.time()
    result = await search("剑来")
    end_time = time.time()
    logger.info(f"Took: {end_time - start_time} s")
    for info in result:
        logger.info(f"{info.title} {info.share_url} {info.last_update_at}")
