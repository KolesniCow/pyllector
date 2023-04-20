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
        self.proxies.update(self.proxy) if proxy is not None else None

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

    @staticmethod
    def _is_valid_content(response: requests.Response) -> bool:
        return False if not response.text and not response.text == 'None' else True

    def _right_main_link(self, main_link):
        return main_link if main_link[-1] == '/' else f'{main_link}/'

    def _is_many_request_error(self, response: requests.Response) -> bool:
        if response.status_code == 429 or response.status_code == 502:
            if not self.astro_link:
                print(
                    f'Too many requests. Repeat request again across {time} seconds.')
                sleep(time)
            else:
                print('429 Http code. Repeat request with new proxy.')
                new_proxy = self.get(self.astro_link).json()['IP']
                print(f'Proxy is change, current ip is {new_proxy}')
                self.proxies.update(self.proxy)
            return True
        return False

    def push(
        self, method: str = '',
        content_type: ContentType = None,
        http_method: HttpMethod = HttpMethod.GET,
        params: dict = None, limit: int = 5, time: float = 60, **kwargs
    ) -> dict | str | None:

        if limit == 0:
            print('Failed get this url. Tries is over')
            return None

        params = self._pull_params_together(params)
        api_link = f'{self.main_api_link}{method}'

        response = self.request(
            http_method.value,
            api_link,
            params=params,
            cookies=self.main_cookies, **kwargs
        )
        
        if self._is_many_request_error(response):
            return self.push(method, content_type, limit=limit-1, time=time, **kwargs)

        if not self._is_valid_content(response):
            print('Response is empty or return None. Try Request again')
            return self.push(method, content_type, limit=limit-1, time=time, **kwargs)

        if self._is_valid_response(response):
            return self._return_content_by_content_type(content_type, response)

        if response.status_code == 400:
            print('Bad Request', response.url)
            return None

        if response.status_code != 429:
            print(
                f'Failed get it url. Status code {response.status_code}.'
                f'URL {response.url}'
            )
            return None


    def _is_valid_response(self, request: Response) -> bool:
        return True if request.status_code == 200 else False
