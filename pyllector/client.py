from time import sleep

import requests
from requests import Session, Response
import urllib.parse
import logging

from pyllector.models import HttpMethod, ContentType


class ApiClient(Session):
    def __init__(
        self, main_api_link: str, main_params: dict = None,
        main_cookie: dict = None, proxy: dict = None, default_time_limit: int = 60,
        default_headers: dict = None, **kwargs
    ) -> None:
        super().__init__(**kwargs)
        self.logger = logging.getLogger('pyllector')
        self.headers.update(default_headers) if default_headers else None
        self.main_api_link = main_api_link
        self.main_api_params = main_params if main_params else {}
        self.main_cookies = main_cookie if main_cookie else {}
        self.proxy = proxy
        self.proxies.update(self.proxy) if proxy is not None else None
        self.default_time_limit = default_time_limit

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

    @staticmethod
    def _is_many_request_error(response: requests.Response) -> bool:
        if response.status_code == 429 or response.status_code == 502:
            return True
        return False

    def push(
        self, method: str = '',
        content_type: ContentType = None,
        http_method: HttpMethod = HttpMethod.GET,
        params: dict = None, limit: int = 5, delay_many_requests: int = 5, **kwargs
    ) -> dict | str | None:

        params = self._pull_params_together(params)
        api_link = urllib.parse.urljoin(self.main_api_link, method)

        if limit == 0:
            self.logger.error(f'Failed get {api_link}. Tries is over')
            return None

        response = self.request(
            http_method.value,
            api_link,
            params=params,
            cookies=self.main_cookies
        )
        
        if self._is_many_request_error(response):
            self.logger.warning(f'Too many requests. Wait {delay_many_requests} sec. '
                                f'Attempts to get content left: {limit}. URL: {response.url}')
            return self.push(method, content_type, limit=limit-1, **kwargs)

        if not self._is_valid_content(response):
            self.logger.warning(f'Response is empty or return None. Attempts to get content left: {limit}. '
                                f'URL: {response.url}. Response body: {response.text}.')
            return self.push(method, content_type, limit=limit-1, **kwargs)

        if self._is_valid_response(response):
            self.logger.info(f'Success get content. URL: {response.url}.')
            return self._return_content_by_content_type(content_type, response)

        if response.status_code != 429:
            self.logger.error(f'Bad Request. URL: {response.url}. Status code: {response.status_code}')
            return None

    @staticmethod
    def _is_valid_response(request: Response) -> bool:
        return True if request.status_code == 200 else False
