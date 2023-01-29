from functools import wraps
from time import asctime,localtime,time
from os import mkdir

import logging

def warp_TimeCounter(org_func):
    @wraps(org_func)
    def wrapper(*args, **kwargs):
        t1 = time()
        resulat = org_func(*args, **kwargs)
        t2 = time() - t1
        print(f"{org_func.__name__} ran in :{t2} sec.")
        return resulat
    return wrapper

def warp_FunctionLogging(org_func):
    if not _mkdir('logging'): return
    logging.basicConfig(filename=f"logging/{org_func.__name__}.log", level=logging.INFO)
    @wraps(org_func)
    def wrapper(*args, **kwargs):
        logging.info(f"[{asctime(localtime(time()))}] Functions {org_func.__name__}, Ran with args: {args}, and kwarts: {kwargs}")
        return org_func(*args, **kwargs)
    return wrapper

def setup_logging(filename: str) -> logging:
    if _mkdir('logging'):
        logger = logging
        logger.basicConfig(filename=f'logging/{filename}', 
            level=logging.INFO,
            encoding='utf-8',
            format='%(asctime)s <%(funcName)s> [%(levelname)s]:%(message)s',
            datefmt='%m/%d/%Y %H:%M:%S')
        return logger
    return

def _mkdir(path: str) -> bool:
    try:
        mkdir(path)
    except FileExistsError:
        return True
    except OSError:
        print("[WARN] Can't access file(ppl don't have promssion)")
        return False
    else:
        return True
