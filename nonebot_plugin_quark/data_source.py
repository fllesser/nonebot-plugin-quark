import re
import httpx
import json
import asyncio
import datetime

class UrlInfo:
    def __init__(
        self,
        title: str,
        share_url: str,
        last_update_at: str = '2000-01-01 00:00:00'
    ):
        self.title = title
        self.share_url = share_url
        self.last_update_at = last_update_at
  
    def __str__(self) -> str:
        return f"{self.title}\n\n{self.share_url}\n\n上次更新: {self.last_update_at}"
    
    def __lt__(self, other):
        return self.last_update_at > other.last_update_at
    

async def search(keyword: str) -> list[UrlInfo]:
    share_id_set = await search_quark_so(keyword)
    #......
    
    url_info_list = [info for share_id in share_id_set if (info := await get_url_info(share_id))]
    return sorted(url_info_list)


async def search_quark_so(keyword: str) -> set[str]:
    url = "https://www.quark.so/s"

    params = {
        'query': keyword
    }
    
    headers = {
        'User-Agent': "Mozilla/5.0 (Linux; Android 10; VOG-AL00 Build/HUAWEIVOG-AL00) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.88 Mobile Safari/537.36",
        'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        'referer': "https://www.quark.so/res/new/zuixinquark",
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
    share_id_set.discard('7c4e2f8ffd44')
    return share_id_set


async def get_url_info(share_id: str) -> UrlInfo:
    url = "https://pan.quark.cn/1/clouddrive/share/sharepage/v2/detail"
    
    params = {
        'pr': "ucpro",
        'fr': "h5",
        'format': "png"
    }
    
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
        "sort": "file_type:asc,updated_at:desc"
    }
    
    headers = {
        'User-Agent': "Mozilla/5.0 (Linux; Android 10; VOG-AL00 Build/HUAWEIVOG-AL00) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.88 Mobile Safari/537.36",
        'Accept': "application/json, text/plain, */*",
        'Accept-Encoding': "gzip, deflate",
        'content-type': "application/json;charset=UTF-8",
        'origin': "https://pan.quark.cn",
        'referer': f"https://pan.quark.cn/s/{share_id}",
    }
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.post(url, params=params, data=json.dumps(payload), headers=headers)
        detail_info = resp.json()['data']['detail_info']
        share = detail_info['share']
    except Exception:
        return None
    try:
        last_update_at = int(detail_info.get('list')[0].get('last_update_at')) // 1000
        last_update_at = format_time(last_update_at)
    except Exception:
        last_update_at = '2000-01-01 00:00:00'
    return UrlInfo(
        title = share.get('title'),
        share_url = share.get('share_url'),
        last_update_at = last_update_at
    )
  
def format_time(timestamp: int) -> str:
    # 将时间戳转换为datetime对象
    dt = datetime.datetime.fromtimestamp(timestamp)
    # 格式化输出为年月日时分秒
    return dt.strftime("%Y-%m-%d %H:%M:%S")
