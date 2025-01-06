import json
import traceback
import sys
from functools import wraps
from typing import Callable, Any

def nullogger(e: Exception):
    pass
    

def nullwrapper(func: Callable) -> Callable:
    @wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        original_excepthook = sys.excepthook
        
        def custom_excepthook(exc_type, exc_value, exc_traceback):
            tb = exc_traceback
            while tb.tb_next:
                tb = tb.tb_next
            if tb.tb_frame.f_code.co_name == func.__name__:
                error_info = {
                    "handled_error": {
                        "type": exc_type.__name__,
                        "message": str(exc_value),
                        "function": func.__name__,
                        "traceback": traceback.format_exc().split('\n'),
                        "args": {
                            "positional": str(args),
                            "keyword": str(kwargs)
                        }
                    }
                }
                print(json.dumps(error_info, indent=2, ensure_ascii=False))
            original_excepthook(exc_type, exc_value, exc_traceback)
        
        sys.excepthook = custom_excepthook
        
        try:
            result = func(*args, **kwargs)
            return result
        finally:
            sys.excepthook = original_excepthook
            
    return wrapper