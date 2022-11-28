## pyllector
Utils for work with api

## Instalation

```Bash
pip install pyllector 
```

## Examples

```Python
from pyllector import ApiCollector
from models import HttpMethod, ContentType

api = ApiCollector('https://some-api.com/v2/', params={'some_api_key': 'some...'})

data = api.push('some_api_method', content_type=ContentType.JSON, http_method=HttpMethod.POST)

print(data['some keys'])

```

ApiCollector check allmost http errors,
 and repeat request `limit` times until he gets response,
  or will return None else `limit` is 0.
