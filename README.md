## pyllector
Modifided aiohttp.ClientSession. More Safety.

## Instalation

```Bash
poetry add git+https://github.com/KolesniCow/pyllector.git#main

# pip install pyllector (For 0.0.6 version)
```

## Example

```Python
from pyllector import ApiClientAsync
from models import HttpMethod, ContentType

import asyncio


async def main():
    api = ApiClientAsync('https://some-api.com/v2/', main_params={'some_api_key': 'some...'})
    data = await api.push('some_api_method',
                        content_type=ContentType.JSON,
                        http_method=HttpMethod.POST,
                        params={'some_method_param': 'some_value'},
                        )
    print(data['some keys'])


asyncio.run(main())

```

ApiCollector check allmost http errors,
 and repeat request `limit` times until he gets response,
 or will return None else `limit` is 0.
