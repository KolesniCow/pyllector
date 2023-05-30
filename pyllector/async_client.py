import asyncio
from time import sleep

import aiohttp

from pyllector.models import HttpMethod, ContentType


class ApiClient:
    def __init__(
            self, main_api_link: str, main_params: dict = None,
            main_cookie: dict = None, proxy: dict = None,
            default_time_limit: int = 60) -> None:
        self.main_api_link = self._right_main_link(main_api_link)
        self.main_api_params = main_params if main_params else {}
        self.main_cookies = main_cookie if main_cookie else {}
        self.proxy = proxy
        self.proxies = self.proxy if proxy is not None else None
        self.default_time_limit = default_time_limit

    def _pull_params_together(self, params: dict = None) -> dict:
        return {**self.main_api_params,  **params} if params is not None else self.main_api_params

    @staticmethod
    def _return_content_by_content_type(
        content_type: ContentType, response: aiohttp.ClientResponse
    ) -> str | dict | aiohttp.ClientResponse:
        if content_type == ContentType.TEXT:
            return response.text

        if content_type == ContentType.JSON:
            return response.json()

        return response

    @staticmethod
    def _is_valid_content(response: aiohttp.ClientResponse) -> bool:
        return False if not response.text and not response.text == 'None' else True

    def _right_main_link(self, main_link):
        return main_link if main_link[-1] == '/' else f'{main_link}/'

    async def _is_many_request_error(self, response: aiohttp.ClientResponse) -> bool:
        if response.status == 429 or response.status == 502:
            print(
                f'Too many requests. Repeat request again across {self.default_time_limit} seconds.')
            await asyncio.sleep(self.default_time_limit)
            return True
        return False

    async def push(
        self, method: str = '',
        content_type: ContentType = None,
        http_method: HttpMethod = HttpMethod.GET,
        params: dict = None, limit: int = 5, **kwargs
    ) -> dict | str | None:

        if limit == 0:
            print('Failed get this url. Tries is over')
            return None

        params = self._pull_params_together(params)
        api_link = f'{self.main_api_link}{method}'

        async with aiohttp.ClientSession(cookies=self.main_cookies) as session:
            async with session.request(
                http_method.value,
                api_link,
                params=params,
                proxy=self.proxies,
                **kwargs
            ) as response:
                if await self._is_many_request_error(response):
                    return await self.push(method, content_type, limit=limit-1, **kwargs)

                if not self._is_valid_content(response):
                    print('Response is empty or return None. Try Request again')
                    return await self.push(method, content_type, limit=limit-1, **kwargs)

                if self._is_valid_response(response):
                    return self._return_content_by_content_type(content_type, response)

                if response.status == 400:
                    print('Bad Request', response.url)
                    return None

                if response.status != 429:
                    print(
                        f'Failed get it url. Status code {response.status}.'
                        f'URL {response.url}'
                    )
                    return None

    def _is_valid_response(self, request: aiohttp.ClientResponse) -> bool:
        return True if request.status == 200 else False
