import json
from functools import wraps

from flask import Response


class ChessResponse(object):
    def __init__(self, data, status="success", http_status_code=200, http_extra_headers=None):
        self.data = data
        self.status = status
        self.http_status_code = http_status_code
        self.http_extra_headers = http_extra_headers

    def dictify(self):
        return {"status": self.status, "data": self.data}


def response_wrapper(func):
    @wraps(func)
    def wrapper(**params):

        try:
            func_result = func(**params)
            if type(func_result) is Response:
                return func_result

            response = ChessResponse(func_result)

        except Exception as err:
            response = ChessResponse(str(err), "error", 500, {})
            print(err)

        return _make_http_response(response.dictify(), response.http_status_code, response.http_extra_headers)

    return wrapper


def _make_http_response(content=None, status_code=200, extra_headers=None, mimetype="application/json"):
    extra_headers = extra_headers or {}

    if content is None:
        content_string = ""
        mimetype = "text/plain"
    else:
        if mimetype == "application/json":
            content_string = json.dumps(content)
        else:
            content_string = content

    return Response(content_string, status_code, extra_headers, mimetype)
