import aiohttp
import functools
import urllib.parse

from schemas.auth import Token
from importlib import import_module
from fastapi import Request, Response, HTTPException, status
from typing import List
import logging
import requests
logger = logging.getLogger()

from network import make_request


def route(
        request_method, path: str, status_code: int,
        payload_key: str, service_url: str,
        authentication_required: bool = False,
        post_processing_func: str = None,
        authentication_token_decoder: str = 'auth.decode_access_token',
        authentication_token_decoder_admin: str = 'auth.decode_access_token_admin',
        authentication_token_decoder_backend_admin: str = 'auth.decode_access_token_backend_admin',
        service_authorization_checker: str = 'auth.is_admin_user',
        service_header_generator: str = 'auth.generate_request_header',
        response_key_to_forge_into_header: str = None,
        keep_header_in_body_after_forging: bool = False,
        response_model: str = None,
        privileges_level: int = 0,
        response_list: bool = False
):

    if response_model:
        response_model = import_function(response_model)
        if response_list:
            response_model = List[response_model]

    app_any = request_method(
        path, status_code=status_code,
        response_model=response_model
    )

    def wrapper(f):
        @app_any
        @functools.wraps(f)
        async def inner(request: Request, response: Response, **kwargs):
            nonlocal service_url  # Dodajemy dostęp do zmiennej z zewnętrznego zakresu
            service_headers = {}
            authorization = None
            
            #logger.info(requests.get("http://user-node-service:3002/workouts"))
            
            if authentication_required:
                authorization = kwargs.get('session_id')
                token_decoder = (
                    import_function(authentication_token_decoder)
                    if privileges_level == 0 else
                    import_function(authentication_token_decoder_admin)
                    if privileges_level == 1 else
                    import_function(authentication_token_decoder_backend_admin)
                )
                
                exc = None
                try:
                    token_payload = await token_decoder(authorization)
                    logger.info(token_payload["valid"])
                    if not token_payload["valid"]:
                        raise HTTPException(
                            status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=token_payload["detail"],
                            headers={'WWW-Authenticate': 'Bearer'},
                        )
                except Exception as e:
                    exc = str(e)
                finally:
                    if exc:
                        raise HTTPException(
                            status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=exc,
                            headers={'WWW-Authenticate': 'Bearer'},
                        )

            scope = request.scope
            method = scope['method'].lower()
            service_path = scope['path']
            request_params = {}
            for param_name, param_value in kwargs.items():
                if param_name != 'session_id' and param_name != payload_key:
                    request_params[param_name] = param_value

            query_params = request.query_params
            if query_params:
                query_string = '?' + str(query_params)
                service_path += query_string

            # Handle payload
            if method in ['post', 'put', 'patch']:
                # For methods that typically have a body, get the payload from kwargs
                payload_obj = kwargs.get(payload_key)
                if payload_obj:
                    if hasattr(payload_obj, 'dict'):
                        payload = payload_obj.dict()
                    elif hasattr(payload_obj, 'model_dump'):
                        payload = payload_obj.model_dump()
                    else:
                        payload = payload_obj
                elif keep_header_in_body_after_forging and authorization:
                    # If no payload but keeping header in body is requested
                    token = Token(session_id=authorization)
                    payload = token.model_dump()
                else:
                    # Include path parameters in the payload for these methods
                    payload = request_params
            else:
                # For other methods (GET, DELETE), don't include a payload
                payload = None

            # Ensure service_url doesn't end with slash and service_path starts with slash
            service_url = service_url.rstrip('/')
            if not service_path.startswith('/'):
                service_path = '/' + service_path

            url = f'{service_url}{service_path}'

            try:
                resp_data, status_code_from_service = await make_request(
                    url=url,
                    method=method,
                    data=payload,
                    headers=service_headers,
                )
            except aiohttp.client_exceptions.ClientConnectorError:
                raise HTTPException(
                    status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                    detail='Service is unavailable.',
                    headers={'WWW-Authenticate': 'Bearer'},
                )

            response.status_code = status_code_from_service

            if all([
                status_code_from_service == status_code,
                post_processing_func
            ]):
                post_processing_f = import_function(post_processing_func)
                resp_data = post_processing_f(resp_data)
            
            if response_key_to_forge_into_header:
                header_value = resp_data.get(response_key_to_forge_into_header)
                if header_value:
                    response.headers[response_key_to_forge_into_header] = str(header_value)
                    del resp_data[response_key_to_forge_into_header]
                    
            return resp_data

        return inner
    return wrapper


def import_function(method_path):
    module, method = method_path.rsplit('.', 1)
    mod = import_module(module)
    return getattr(mod, method, lambda *args, **kwargs: None)