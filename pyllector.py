import asyncio
import aiohttp
from models import HttpMethod, ContentType


class ApiCollector:
    def __init__(self, main_api_link: str, main_params: dict = None):
        self.main_api_link = main_api_link
        self.main_api_params = main_params
        self.session = aiohttp.ClientSession()
    
    def pull_params_together(self, params: dict = None) -> dict:
        return {**self.main_api_params,  **params} if params is not None else self.main_api_params
    
    async def push(self, method: str = '/', content_type: ContentType = ContentType.TEXT,
                   http_method: HttpMethod = HttpMethod.GET,
                   params: dict = None, limit: int = 5,
                   time: float = 60, **kwargs) -> dict | str | None:
        
        if limit == 0:
            print('Failed get this url. Tries is over')
            return None
        
        params = self.pull_params_together(params)
        
        async with self.session.request(http_method.value, f'{self.main_api_link}{method}', params=params, **kwargs) as response:
            if response.status != 400:
                if self.is_valid_response(response):
                    if content_type == ContentType.TEXT:
                        return await response.text()
                    if content_type == ContentType.JSON:
                        return await response.json()
                else:
                    if response.status != 429:
                        print(f'Failed get it url. Status code {response.status}. URL {response.url}')
                    else:
                        print(f'429 Http code. Repeat request again across {time} seconds.')
                        await asyncio.sleep(time)
                    return await self.push(method, content_type, limit=limit-1 **kwargs)
            else:
                print('Bad Request', response.url)
                return None
            
    def is_valid_response(self, request) -> bool:
        return True if request.status == 200 else False
        

    
