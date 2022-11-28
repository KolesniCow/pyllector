import asyncio
import aiohttp
from models import HttpMethod, ContentType


class ApiCollector:
    def __init__(self, main_api_link: str, main_params: str = None):
        self.main_api_link = main_api_link
        self.main_api_params = main_params
        self.session = aiohttp.ClientSession()
    
    def pull_params_together(self, params: dict = None) -> dict:
        return {**self.main_api_params,  **params} if params is not None else self.main_api_params
    
    async def push(self, method: str, content_type: ContentType,
                   http_method: HttpMethod = HttpMethod.GET,
                   params: dict = None, **kwargs) -> dict | str:
        
        params = self.pull_params_together(params)
        
        async with self.session.request(http_method.value, f'{self.main_api_link}/{method}', params=params, **kwargs) as response:    
            if content_type == ContentType.TEXT:
                return await response.text
            if content_type == ContentType.JSON:
                return await response.json

    async def get_until_http_code(self, method: str, http_method: HttpMethod,
                            limit: int = 5, time: float = 10,
                            params: dict = None, http_code: int = 200) -> str | None | dict:
        req = await self.push_request(method, http_method, params)
        if limit != 0 and str(req.status_code) != str(http_code):
            await asyncio.sleep(time)
            return await self.get_until_http_code(method, http_method, limit-1, params=params)
        elif str(req.status_code) == str(http_code):
            return req
        elif limit == 0:
            return None
    
    
