def update_query_params(params: dict, **kwargs) -> dict:
    for key, value in kwargs.items():
        if value:
            params[key] = value
    return params
