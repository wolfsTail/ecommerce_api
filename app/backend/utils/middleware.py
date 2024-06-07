from uuid import uuid4
from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware


class LogginMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, logging_instance) -> None:
        super().__init__(app)
        self.logging_instance = logging_instance
    
    async def dispatch(self, request: Request, call_next):
        log_id = str(uuid4())
        with self.logging_instance.contextualize(log_id=log_id):
            try:
                response = await call_next(request)
                if response.status_code in [401, 402, 403, 404]:
                    self.logging_instance.warning(f"Запрос к {request.url.path} провален")
                else:
                    self.logging_instance.info('Успешный доступ ' + request.url.path)
            except Exception as err:
                self.logging_instance.error(f"Запрос к {request.url.path} провален: {err}")
                response = JSONResponse(content={"success": False}, status_code=500)
            return response       
