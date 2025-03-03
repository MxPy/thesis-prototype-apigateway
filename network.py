import aiohttp
import async_timeout

from conf import settings


async def make_request(
    url: str,
    method: str,
    data: dict = None,
    headers: dict = None
):
    if not data:
        data = {}

    with async_timeout.timeout(settings.GATEWAY_TIMEOUT):
        async with aiohttp.ClientSession() as session:
            request = getattr(session, method)
            async with request(url, json=data, headers=headers) as response:
                if response.status == 404:
                    return ({}, response.status)
                try:
                    data = await response.json()
                    return (data, response.status)
                except:
                    return ("error", response.status)