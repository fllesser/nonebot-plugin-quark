import asyncio
import datetime
import re

import httpx
from tenacity import retry, stop_after_attempt, wait_fixed


class UrlInfo:
    def __init__(self, title: str, keyword: str, share_url: str, last_update_at: str):
        self.title = title
        self.keyword = keyword
        self.share_url = share_url
        self.last_update_at = last_update_at

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


async def search(keyword: str) -> list[UrlInfo]:
    # 并发搜索 local_share_id_set 和 entire_share_id_set
    tasks = [search_quark_so(keyword), search_quark_so(keyword, 2)]
    local_share_id_set, entire_share_id_set = await asyncio.gather(*tasks)

    share_id_set = local_share_id_set | entire_share_id_set
    # 使用 asyncio.gather 并发获取 url_info, 并过滤掉 None
    url_info_list = await asyncio.gather(*[get_url_info(keyword, share_id) for share_id in share_id_set])
    # 过滤掉 None
    url_info_list = [info for info in url_info_list if info is not None]
    return sorted(url_info_list)


@retry(stop=stop_after_attempt(3), wait=wait_fixed(4))
async def search_quark_so(keyword: str, type: int = 1) -> set[str]:
    url = "https://www.quark.so/s"

    params = {"query": keyword, "type": type}

    headers = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 10; VOG-AL00 Build/HUAWEIVOG-AL00) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.88 Mobile Safari/537.36",  # noqa: E501
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",  # noqa: E501
        "referer": "https://www.quark.so/res/new/zuixinquark",
    }

    async with httpx.AsyncClient() as client:
        resp = await client.get(url, params=params, headers=headers)
    return get_ids_from_text(resp.text)


def get_ids_from_text(text: str) -> set[str]:
    # 正则表达式模式
    pattern = r"https://pan\.quark\.cn/s/([a-zA-Z0-9]+)"
    # 使用 findall 方法查找所有匹配的 URL id，并转换为集合
    share_id_set = set(re.findall(pattern, text))
    # 移除特定的 id
    share_id_set.discard("7c4e2f8ffd44")
    return share_id_set


async def get_url_info(keyword: str, share_id: str) -> UrlInfo | None:
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
        async with httpx.AsyncClient() as client:
            resp = await client.post(url, params=params, json=payload, headers=headers)
        detail_info = resp.json()["data"]["detail_info"]
        share = detail_info["share"]
    except Exception:
        return None
    try:
        last_update_at = int(detail_info.get("list")[0].get("last_update_at")) // 1000
        last_update_at = format_time(last_update_at)
    except Exception:
        last_update_at = "2000-01-01 00:00:00"
    return UrlInfo(
        title=share.get("title"),
        keyword=keyword,
        share_url=share.get("share_url"),
        last_update_at=last_update_at,
    )


def format_time(timestamp: int) -> str:
    # 将时间戳转换为datetime对象
    dt = datetime.datetime.fromtimestamp(timestamp)
    # 格式化输出为年月日时分秒
    return dt.strftime("%Y-%m-%d %H:%M:%S")
