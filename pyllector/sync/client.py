from time import sleep

import requests
from requests import Session, Response

from pyllector.models import HttpMethod, ContentType


class ApiClient(Session):
    def __init__(
        self, main_api_link: str, main_params: dict = None,
        main_cookie: dict = None, proxy: dict = None,
        astro_proxy_change_link: str = None,  **kwargs
    ) -> None:
        super().__init__(**kwargs)
        self.main_api_link = self._right_main_link(main_api_link)
        self.main_api_params = main_params if main_params else {}
        self.main_cookies = main_cookie if main_cookie else {}
        self.astro_link = astro_proxy_change_link
        self.proxy = proxy
        self.proxies.update(self.proxy)

    def _pull_params_together(self, params: dict = None) -> dict:
        return {**self.main_api_params,  **params} if params is not None else self.main_api_params

    @staticmethod
    def _return_content_by_content_type(
        content_type: ContentType, response: Response
    ) -> str | dict | requests.Response:
        if content_type == ContentType.TEXT:
            return response.text

        if content_type == ContentType.JSON:
            return response.json()

        return response

    def _right_main_link(self, main_link):
        return main_link if main_link[-1] == '/' else f'{main_link}/'

    def push(
        self, method: str = '',
        content_type: ContentType = ContentType.TEXT,
        http_method: HttpMethod = HttpMethod.GET,
        params: dict = None, limit: int = 5, time: float = 60, **kwargs
    ) -> dict | str | None:

        if limit == 0:
            print('Failed get this url. Tries is over')
            return None

        params = self._pull_params_together(params)
        response = self.request(
            http_method.value,
            f'{self.main_api_link}{method}',
            params=params,
            cookies=self.main_cookies, **kwargs
        )
        if response.status_code != 400:
            if self._is_valid_response(response):
                return self._return_content_by_content_type(
                    content_type, response
                )
            else:
                if response.status_code != 429:
                    print(
                        f'Failed get it url. Status code {response.status_code}.'
                        f'URL {response.url}'
                    )
                else:
                    if not self.astro_link:
                        print(f'429 Http code. Repeat request again across {time} seconds.')
                        sleep(time)
                    else:
                        print('429 Http code. Repeat request with new proxy.')
                        new_proxy = self.get(self.astro_link).json()['IP']
                        print(f'Proxy is change, current ip is {new_proxy}')
                        self.proxies.update(self.proxy)
                        self.get('https://google.com')
                return self.push(method, content_type, limit=limit-1, time=time, **kwargs)
        else:
            print('Bad Request', response.url)
            return None

    def _is_valid_response(self, request: Response) -> bool:
        return True if request.status_code == 200 else False
