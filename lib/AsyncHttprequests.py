import traceback
from typing import Any
import aiohttp
from core.logger import Logger, LogLevel
from schemas.exception import BizException

import aiohttp
import traceback
from json import JSONDecodeError

from core.logger import Logger, LogLevel


async def response_handler(*, response: aiohttp.ClientResponse, url: str, **kwargs):
    if response.status >= 400:
        text = await response.text()
        Logger.log(LogLevel.WARN, f"{response.method} {url}", kwargs, None, text)
        raise BizException(
            status_code=response.status,
            message=text
        )
    else:
        try:
            return await response.json()
        except:
            return await response.text()

class BaseAsyncHttpService:
    @staticmethod
    async def _get(*, session: aiohttp.ClientSession, url: str, params=None, **kwargs) -> Any:
        try:
            async with session.get(url, params=params, **kwargs) as resp:
                return await response_handler(
                    response=resp,
                    url=url,
                    params=params,
                    **kwargs
                )
        except aiohttp.ClientConnectorError as e:
            tb = traceback.format_exc()
            Logger.log(LogLevel.ERROR, f"{resp.method} {url}", kwargs | {'params': params}, None, tb)
            raise BizException(status_code=500, message=str(e.args))
    @staticmethod
    async def _post(*, session: aiohttp.ClientSession, url: str, data=None, json=None, **kwargs) -> Any:
        try:
            async with session.post(url, data=data, json=json, **kwargs) as resp:
                return await response_handler(
                    response=resp,
                    url=url,
                    data=data,
                    json=json,
                    **kwargs
                )
        except aiohttp.ClientConnectorError as e:
            tb = traceback.format_exc()
            Logger.log(LogLevel.ERROR, f"{resp.method} {url}", kwargs | {"data": data, "json": json}, None, tb)
            raise BizException(status_code=500, message=str(e.args))
    @classmethod
    async def get(cls, *, url: str, params=None, session: aiohttp.ClientSession = None, **kwargs):
        if session is None:
            async with aiohttp.ClientSession() as session:
                return await cls._get(session=session, url=url, params=params, **kwargs)
        else:
            return await cls._get(session=session, url=url, params=params, **kwargs)
    @classmethod
    async def post(cls, *, url: str, data=None, json=None, session: aiohttp.ClientSession = None, **kwargs):
        if session is None:
            async with aiohttp.ClientSession() as session:
                return await cls._post(session=session, url=url, data=data, json=json, **kwargs)
        else:
            return await cls._post(session=session, url=url, data=data, json=json, **kwargs)