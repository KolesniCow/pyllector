## pyllector
Modifided requests.Session. More Safety.

## Instalation

```Bash
# poetry
poetry add git+https://github.com/KolesniCow/pyllector.git#main

# pip
pip install git+https://github.com/KolesniCow/pyllector.git#main
```

## Example

```Python
from pyllector import ApiClient
from models import HttpMethod, ContentType


def main():
    api = ApiClient('https://some-api.com/v2/', main_params={'some_api_key': 'some...'})
    data =  api.push('some_api_method',
                        content_type=ContentType.JSON,
                        http_method=HttpMethod.POST,
                        params={'some_method_param': 'some_value'},
                        )
    print(data['some keys'])

if __name__ == '__main__':
    main()
```

ApiCollector check allmost http errors,
 and repeat request `limit` times until he gets response,
 or will return None else `limit` is 0.
