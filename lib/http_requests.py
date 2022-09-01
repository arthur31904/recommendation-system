import requests
from core.logger import Logger, LogLevel
import traceback
from schemas.exception import BizException


def get_and_log(url):
        try:
            check_requests = requests.get(url)
            Logger.log(LogLevel.INFO, "get_and_log", url, None, "success")
            return check_requests
        except BizException as e:
            tb = traceback.format_exc()
            Logger.log(LogLevel.WARN, "get_and_log", url, e.message, tb)
            raise BizException(
                status_code=500,
                message=str(e.args)
            )
        except Exception as e:
            tb = traceback.format_exc()
            Logger.log(LogLevel.WARN, "get_and_log", url, e, tb)
            raise BizException(
                status_code=500,
                message=str(e.args)
            )

def post_and_log(url, data, headers):
        try:
            check_requests = requests.post(url, json=data, headers=headers)
            Logger.log(LogLevel.INFO, "post_and_log", data, None, "success")

            return check_requests
        except BizException as e:
            tb = traceback.format_exc()
            Logger.log(LogLevel.WARN, "post_and_log", data, e.message, tb)
            raise BizException(
                status_code=500,
                message=str(e.args)
            )
        except Exception as e:
            tb = traceback.format_exc()
            Logger.log(LogLevel.WARN, "post_and_log", data, e, tb)
            raise BizException(
                status_code=500,
                message=str(e.args)
            )