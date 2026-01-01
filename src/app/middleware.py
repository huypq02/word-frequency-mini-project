from starlette import status
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response
from starlette.types import ASGIApp
import re

ALLOWED_METHODS = ['POST', 'PUT', 'PATCH']

def get_content_type_from_body(body: bytes) -> str | None:
    content_type_match = re.search(rb'Content-Type: ([^\r\n]+)', body)
    if content_type_match:
        return content_type_match.group(1).decode("utf-8")
    return None

def set_body(request: Request, body: bytes):
    async def receive():
        return {"type": "http.request", "body": body}
    request._receive = receive # Restore the body so downstream code can read it again

async def get_body(request: Request) -> bytes:
    body = await request.body()
    set_body(request, body)
    return body

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

class LimitUploadContentType(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp, allowed_content_type: list = None) -> None:
        super().__init__(app)
        self.allowed_content_type = allowed_content_type

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        if request.method in ALLOWED_METHODS:
            content_type = request.headers.get("Content-Type", "")

            if content_type.startswith("multipart/form-data"):
                try:
                    bd = await get_body(request)
                    file_content_type = get_content_type_from_body(bd)
                except (RuntimeError, ValueError) as e:
                    print(f"Error processing request body: {e}")
                    return Response(status_code=status.HTTP_400_BAD_REQUEST,
                                    content='{"detail":"Error reading or parsing request body."}',
                                    media_type="application/json") 
            
                if not file_content_type:
                    return Response(status_code=status.HTTP_400_BAD_REQUEST,
                                    content='{"detail":"Content-Type from request body is not found."}',
                                    media_type="application/json")
                
                if file_content_type not in self.allowed_content_type:
                    return Response(status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
                                    content='{"detail":"Uploaded file type is not allowed."}',
                                    media_type="application/json")
        return await call_next(request)
