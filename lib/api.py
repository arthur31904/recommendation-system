# coding=utf8
from __future__ import unicode_literals
import datetime
import logging
import time

from pyramid.response import Response
from .my_exception import MyException

def return_format(some_view):
    def wrapper(context, request):
        system_name = request.registry.settings.get('system_name', '')
        logger = logging.getLogger(system_name)
        content_type = str('application/json')
        start = time.time()
        try:
            r = some_view(context, request)
            stop = time.time()
            run_time = stop - start
            j = format_processor(**r.json)
            j['server_time_consumed'] = float('{:.2f}'.format(run_time)) # 小數點第二位
            r.json = j
            r.content_type = content_type
            logger_json = {"route_name ": system_name.lower() + "." + request.route_name,
                           "method": request.method,
                           "path_url": request.path_url,
                           "ip": request.real_ip,
                           "run_time": run_time}
            # check user type
            if request.member_id:
                logger_json['user'] = str(request.member_id)

            logger.info(logger_json)
            request.db_session.close()
            return r
        except MyException as err:
            stop = time.time()
            run_time = stop - start
            logger_json = {"route_name ": system_name.lower() + "." + request.route_name,
                           "method": request.method,
                           "path_url": request.path_url,
                           "ip": request.real_ip,
                           "run_time": run_time,
                           "err_message": err.message,
                           "err_code": err.code,
                           "err_source": err.source}
            # check user type
            if request.member_id:
                logger_json['user'] = str(request.member_id)

            logger.warning(logger_json)
            logger_json["err_message"] = err.message
            request.db_session.rollback()
            return Response(content_type=content_type,
                            json_body=format_processor(err=err))
        except Exception as err:
            stop = time.time()
            run_time = stop - start
            logger_json = {"route_name ": system_name.lower() + "." + request.route_name,
                           "method": request.method,
                           "path_url": request.path_url,
                           "ip": request.real_ip,
                           "run_time": run_time,
                           "err": err.args[0] if err.args else "",
                           # "err_code": err.code if err.code else ""
                           }
            # check user type
            if request.member_id:
                logger_json['user'] = str(request.member_id)

            logger.warning(logger_json)
            request.db_session.rollback()
            return Response(content_type=content_type,
                            json_body=format_processor(err=err))

    return wrapper


def format_processor(response=None, message=None, code=None, err=None, **kwargs):
    """

    :param response: 回傳值
    :param err: 錯誤處理

    :return code: 錯誤代碼
    :return message: 錯誤訊息
    """
    if err:
        code, message, status_report = \
            getattr(err, 'code', 400), str(err), False

        if hasattr(err, 'unpack_errors'):
            code = 400  # HTTPBadRequest
            func = getattr(err, 'unpack_errors')
            message = func()
    else:
        code, message, status_report = code if code else 200, message if message else None, True

    return {'status': status_report, 'code': code, 'message': message,
            'server_time': int(time.mktime(datetime.datetime.utcnow().timetuple())), 'response': response}
