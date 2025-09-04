from nonebot.log import logger
import pytest


@pytest.mark.asyncio
async def test_search():
    import time

    from nonebot_plugin_quark.data_source import QuarkSearch

    start_time = time.time()
    async with QuarkSearch("基地3") as client:
        result = await client.search()
    end_time = time.time()
    logger.info(f"Took: {end_time - start_time} s")
    assert result
    for info in result:
        logger.info(f"{info.title} 最后更新时间: {info.last_update_at}")
        logger.info(f"  🔗：{info.share_url}")
        logger.info(f"  相关度: {info.relevance}")
