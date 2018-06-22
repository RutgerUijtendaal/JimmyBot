#!/usr/local/bin/python3

import asyncio
import aiohttp


async def download_page(url):
    headers = {}
    headers['User-Agent'] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36"
    loop = asyncio.get_event_loop()
    try:
        async with aiohttp.ClientSession(loop=loop) as session:
            async with session.get(url, headers=headers) as r:
                if r.status == 200:
                    return await r.text()
    except Exception:
        return None
