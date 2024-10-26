import aiohttp
import functools

from schemas.auth import Token
from importlib import import_module
from fastapi import Request, Response, HTTPException, status
from typing import List
import logging
logger = logging.getLogger()

#from exceptions import (AuthTokenMissing, AuthTokenExpired, AuthTokenCorrupted)
from network import make_request

#test
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
    """
    it is an advanced wrapper for FastAPI router, purpose is to make FastAPI
    acts as a gateway API in front of anything

    Args:
        request_method: is a callable like (app.get, app.post and so on.)
        path: is the path to bind (like app.post('/api/users/'))
        status_code: expected HTTP(status.HTTP_200_OK) status code
        payload_key: used to easily fetch payload data in request body
        authentication_required: is bool to give to user an auth priviliges
        post_processing_func: does extra things once in-network service returns
        authentication_token_decoder: decodes JWT token as a proper payload
        service_authorization_checker: does simple front authorization checks
        service_header_generator: generates headers for inner services from jwt token payload # noqa
        response_model: shows return type and details on api docs
        response_list: decides whether response structure is list or not

    Returns:
        wrapped endpoint result as is

    """

    # request_method: app.post || app.get or so on
    # app_any: app.post('/api/login', status_code=200, response_model=int)
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
            service_headers = {}
            
            #TODO: connect it to aa server
            if authentication_required:
                
                # authentication
                #authorization = request.headers.get('Authorization')
                authorization = kwargs.get('session_id')
                token_decoder = (
                    import_function(authentication_token_decoder)
                    if privileges_level == 0 else
                    import_function(authentication_token_decoder_admin)
                    if privileges_level == 1 else
                    import_function(authentication_token_decoder_backend_admin)
                )
                
                # raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                #             detail=f'{authorization}')
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
                    # in case a new decoder is used by dependency injection and
                    # there might be an unexpected error
                    exc = str(e)
                finally:
                    if exc:
                        raise HTTPException(
                            status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=exc,
                            headers={'WWW-Authenticate': 'Bearer'},
                        )
                
                # # authorization
                # if service_authorization_checker:
                #     authorization_checker = import_function(
                #         service_authorization_checker
                #     )
                #     is_user_eligible = authorization_checker(token_payload)
                #     if not is_user_eligible:
                #         raise HTTPException(
                #             status_code=status.HTTP_403_FORBIDDEN,
                #             detail='You are not allowed to access this scope.',
                #             headers={'WWW-Authenticate': 'Bearer'},
                #         )

                # # service headers
                # if service_header_generator:
                #     header_generator = import_function(
                #         service_header_generator
                #     )
                #     service_headers = header_generator(token_payload)

            scope = request.scope

            method = scope['method'].lower()
            path = scope['path']

            payload_obj = kwargs.get(payload_key)
            if keep_header_in_body_after_forging:
                token = Token(session_id = authorization)
                payload = payload_obj.dict() if payload_obj else token.model_dump()
            else:
                payload = payload_obj.dict() if payload_obj else {}

            
            url = f'{service_url}{path}'

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
            # except aiohttp.client_exceptions.ContentTypeError:
            #     raise HTTPException(
            #         status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            #         detail='Service error.',
            #         headers={'WWW-Authenticate': 'Bearer'},
            #     )

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

    return wrapper


def import_function(method_path):
    module, method = method_path.rsplit('.', 1)
    mod = import_module(module)
    return getattr(mod, method, lambda *args, **kwargs: None)