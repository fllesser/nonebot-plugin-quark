import asyncio
from dataclasses import dataclass
import datetime
import re
from typing_extensions import override

import httpx
from nonebot.log import logger


@dataclass
class UrlInfo:
    title: str
    keyword: str
    share_url: str
    last_update_at: str

    @override
    def __str__(self) -> str:
        return f"标题: {self.title}\n链接: {self.share_url}\n更新时间: {self.last_update_at}"

    def __lt__(self, other):
        return self.relevance > other.relevance

    @property
    def relevance(self) -> int:
        # 将关键词拆成单个汉字
        chars = list(self.keyword)
        # 计算每个汉字在标题中出现的次数
        return sum(self.title.count(char) for char in chars)


class QuarkSearch:
    def __init__(self, keyword: str):
        self.keyword = keyword

    async def __aenter__(self):
        self.client = httpx.AsyncClient(timeout=30)
        # 可能还需要其他初始化
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.client:
            await self.client.aclose()

    async def search(self) -> list[UrlInfo]:
        # 并发搜索 local_share_id_set 和 entire_share_id_set
        tasks = [self._quark_so(), self._quark_so(2)]
        local_share_id_set, entire_share_id_set = await asyncio.gather(*tasks)
        logger.debug(f"local_share_id_set: {local_share_id_set}")
        logger.debug(f"entire_share_id_set: {entire_share_id_set}")

        share_id_set = local_share_id_set | entire_share_id_set
        # 使用 asyncio.gather 并发获取 url_info, 并过滤掉 None
        tasks = [self._get_url_info(self.keyword, share_id) for share_id in share_id_set]
        url_info_list = await asyncio.gather(*tasks)
        # 过滤掉 None
        url_info_list = [info for info in url_info_list if info is not None]
        return sorted(url_info_list)

    # @retry(stop=stop_after_attempt(3), wait=wait_fixed(4))
    async def _quark_so(self, type: int = 1) -> set[str]:
        url = "https://www.quark.so/s"

        params = {"query": self.keyword, "type": type}

        headers = {
            "User-Agent": "Mozilla/5.0 (Linux; Android 10; VOG-AL00 Build/HUAWEIVOG-AL00) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.88 Mobile Safari/537.36",  # noqa: E501
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",  # noqa: E501
            "referer": "https://www.quark.so/res/new/zuixinquark",
        }

        resp = await self.client.get(url, params=params, headers=headers)
        return self._get_ids_from_text(resp.text)

    def _get_ids_from_text(self, text: str) -> set[str]:
        # 正则表达式模式
        pattern = r"https://pan\.quark\.cn/s/([a-zA-Z0-9]+)"
        # 使用 findall 方法查找所有匹配的 URL id，并转换为集合
        share_id_set = set(re.findall(pattern, text))
        # 移除特定的 id
        share_id_set.discard("7c4e2f8ffd44")
        return share_id_set

    async def _get_url_info(self, keyword: str, share_id: str) -> UrlInfo | None:
        url = "https://pan.quark.cn/1/clouddrive/share/sharepage/v2/detail"

        params = {"pr": "ucpro", "fr": "h5", "format": "png"}

        payload = {
            "pwd_id": share_id,
            "pdir_fid": "0",
            "force": 0,
            "page": 1,
            "size": 50,
            "fetch_banner": 1,
            "fetch_share": 1,
            "fetch_total": 1,
            "fetch_sub_file_cnt": 1,
            "sort": "file_type:asc,updated_at:desc",
        }

        headers = {
            "User-Agent": "Mozilla/5.0 (Linux; Android 10; VOG-AL00 Build/HUAWEIVOG-AL00) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.88 Mobile Safari/537.36",  # noqa: E501
            "Accept": "application/json, text/plain, */*",
            "Accept-Encoding": "gzip, deflate",
            "content-type": "application/json;charset=UTF-8",
            "origin": "https://pan.quark.cn",
            "referer": f"https://pan.quark.cn/s/{share_id}",
        }
        try:
            resp = await self.client.post(url, params=params, json=payload, headers=headers)
            detail_info = resp.json()["data"]["detail_info"]
            detail_info = DetailInfo(**detail_info)
        except Exception:
            return None
        try:
            last_update_at = int(detail_info.list[0].last_update_at) // 1000
            last_update_at = self.format_time(last_update_at)
        except Exception:
            last_update_at = "2000-01-01 00:00:00"
        return UrlInfo(
            title=detail_info.share.title,
            keyword=keyword,
            share_url=detail_info.share.share_url,
            last_update_at=last_update_at,
        )

    def format_time(self, timestamp: int) -> str:
        # 将时间戳转换为datetime对象
        dt = datetime.datetime.fromtimestamp(timestamp)
        # 格式化输出为年月日时分秒
        return dt.strftime("%Y-%m-%d %H:%M:%S")


from pydantic import BaseModel


class File(BaseModel):
    fid: str
    file_name: str
    last_update_at: int


class Share(BaseModel):
    title: str
    share_url: str
    created_at: int
    updated_at: int


class DetailInfo(BaseModel):
    is_owner: int
    share: Share
    list: list[File]
