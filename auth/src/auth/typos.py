from typing import TYPE_CHECKING
from fastapi.requests import Request as FastAPIRequest
if TYPE_CHECKING:
    from .app import App



class Request(FastAPIRequest):
    app: "App" = ...