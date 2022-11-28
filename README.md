## pyllector
Utils for work with api

## Instalation

```Bash
pip install pyllector 
```

## Example

```Python
from pyllector import ApiCollector
from models import HttpMethod, ContentType

api = ApiCollector('https://some-api.com/v2/', main_params={'some_api_key': 'some...'})

data = api.push('some_api_method', content_type=ContentType.JSON, http_method=HttpMethod.POST, params={'some_method_param': 'some_value'})

print(data['some keys'])

```

ApiCollector check allmost http errors,
 and repeat request `limit` times until he gets response,
  or will return None else `limit` is 0.
