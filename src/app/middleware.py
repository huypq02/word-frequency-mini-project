from starlette import status
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response
from starlette.types import ASGIApp


ALLOWED_METHODS = ['POST','PUT','PATCH']

class LimitUploadSize(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp, max_upload_size: int = 5_000_000) -> None:
        super().__init__(app)
        self.max_upload_size = max_upload_size

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        if request.method in ALLOWED_METHODS:
            if 'content-length' not in request.headers:
                return Response(status_code=status.HTTP_411_LENGTH_REQUIRED,
                                content='{"detail":"Content-Length header is required for file uploads."}',
                                media_type="application/json")
            content_length_header = request.headers['content-length']
            
            try:
                content_length = int(content_length_header)
            except ValueError:
                print("Error while converting the content-length header to integer.")
                return Response(status_code=status.HTTP_400_BAD_REQUEST,
                                content='{"detail":"Content-Length should be a numeric value"}',
                                media_type="application/json")

            if content_length > self.max_upload_size:
                return Response(status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                                content='{"detail":"Uploaded content exceeds the maximum allowed size."}',
                                media_type="application/json")
        return await call_next(request)
