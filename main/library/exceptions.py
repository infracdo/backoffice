from fastapi import Request
from fastapi.responses import JSONResponse

class RequestException(Exception):
    def __init__(self, *, message: str, status: str = "error", **kwargs: str):
        self.status = status
        self.message = message
        self.others = kwargs