from enum import Enum


class HttpMethod(Enum):
    GET = 'GET'
    POST = 'POST'
    PUT = 'PUT'
    DELETE = 'DELETE'
    
    
class ContentType(Enum):
    TEXT = 1
    JSON = 2