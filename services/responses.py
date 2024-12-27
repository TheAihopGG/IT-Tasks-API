from fastapi.responses import JSONResponse

class ErrorResponse(JSONResponse):
    def __init__(
        self,
        msg: str,
        content = None,
        status_code = 404,
        headers = None,
        media_type = None,
        background = None
    ):
        content = {
            "detail":{
                "msg":msg
            }
        }
        super().__init__(content, status_code, headers, media_type, background)
