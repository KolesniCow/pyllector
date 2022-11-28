import asyncio
import aiohttp
from models import HttpMethod


class ApiCollector:
    def __init__(self, main_api_link: str, main_params: str = None, cookie: dict = None):
        self.main_api_link = main_api_link
        self.main_api_params = main_params
        self.cookie = cookie
        self.session = Session()

    def push_request(self, method: str, http_method: HttpMethod, params: dict = None) -> Response:
        params = {**self.main_api_params,  **params} if params is not None else self.main_api_params
        return self.session.request(http_method.value,
                                    f'{self.main_api_link}/{method}',
                                    cookies=self.cookie,
                                    params=params)

    def get_json_content(self, method: str, http_method: HttpMethod, params: dict = None) -> dict:
        return self.push_request(method, http_method, params).json()

    def get_html_content(self, method: str, http_method: HttpMethod, params: dict = None) -> BeautifulSoup:
        html = self.push_request(method, http_method, params).text
        return BeautifulSoup(html, 'html.parser')

    def get_until_http_code(self, method: str, http_method: HttpMethod,
                            limit: int = 5, time: float = 10,
                            params: dict = None, http_code: int = 200) -> Response | None:
        req = self.push_request(method, http_method, params)
        if limit != 0 and str(req.status_code) != str(http_code):
            sleep(time)
            return self.get_until_http_code(method, http_method, limit-1, time, params, http_code)
        elif str(req.status_code) == str(http_code):
            return req
        elif limit == 0:
            return None
