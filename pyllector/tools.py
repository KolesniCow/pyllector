def setup_query_params(**kwargs) -> dict:
    params = {}
    for key, value in kwargs.items():
        if value:
            params[key] = value
    return params
