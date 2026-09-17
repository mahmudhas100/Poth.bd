import time
from collections import defaultdict
from typing import Dict, List, Tuple
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse

class SecurityAndRateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)
        # Store: ip -> list of timestamps
        self.search_requests: Dict[str, List[float]] = defaultdict(list)
        self.general_requests: Dict[str, List[float]] = defaultdict(list)
        self.last_cleanup = time.time()

        # Configurable limits
        self.SEARCH_LIMIT = 60  # max requests per minute for /search
        self.GENERAL_LIMIT = 120  # max requests per minute for other endpoints
        self.WINDOW_SECONDS = 60.0

    def get_client_ip(self, request: Request) -> str:
        # Fly.io header
        fly_ip = request.headers.get("fly-client-ip")
        if fly_ip:
            return fly_ip.strip()

        # Cloudflare / reverse proxy header
        cf_ip = request.headers.get("cf-connecting-ip")
        if cf_ip:
            return cf_ip.strip()

        # X-Forwarded-For header
        x_forwarded = request.headers.get("x-forwarded-for")
        if x_forwarded:
            return x_forwarded.split(",")[0].strip()

        # Fallback to direct client host
        if request.client and request.client.host:
            return request.client.host

        return "unknown"

    def cleanup_old_entries(self, current_time: float):
        """Periodically prune stale IP timestamps to avoid memory growth."""
        cutoff = current_time - self.WINDOW_SECONDS
        
        for ip in list(self.search_requests.keys()):
            self.search_requests[ip] = [t for t in self.search_requests[ip] if t > cutoff]
            if not self.search_requests[ip]:
                del self.search_requests[ip]

        for ip in list(self.general_requests.keys()):
            self.general_requests[ip] = [t for t in self.general_requests[ip] if t > cutoff]
            if not self.general_requests[ip]:
                del self.general_requests[ip]

    async def dispatch(self, request: Request, call_next) -> Response:
        path = request.url.path
        now = time.time()

        # Run periodic cleanup every 60s
        if now - self.last_cleanup > 60:
            self.cleanup_old_entries(now)
            self.last_cleanup = now

        # Exempt health check from rate limiting so Fly.io checks never get dropped
        if path == "/health" or path == "/":
            response = await call_next(request)
            self._apply_security_headers(response)
            return response

        client_ip = self.get_client_ip(request)

        # Apply specific rate limits by route
        if path.startswith("/search"):
            timestamps = self.search_requests[client_ip]
            cutoff = now - self.WINDOW_SECONDS
            # Filter timestamps within window
            self.search_requests[client_ip] = [t for t in timestamps if t > cutoff]

            if len(self.search_requests[client_ip]) >= self.SEARCH_LIMIT:
                return JSONResponse(
                    status_code=429,
                    content={"detail": "Too many search requests. Please wait a moment."},
                    headers={
                        "Retry-After": "10",
                        "X-RateLimit-Limit": str(self.SEARCH_LIMIT),
                        "X-RateLimit-Remaining": "0"
                    }
                )

            self.search_requests[client_ip].append(now)

        else:
            timestamps = self.general_requests[client_ip]
            cutoff = now - self.WINDOW_SECONDS
            self.general_requests[client_ip] = [t for t in timestamps if t > cutoff]

            if len(self.general_requests[client_ip]) >= self.GENERAL_LIMIT:
                return JSONResponse(
                    status_code=429,
                    content={"detail": "Too many requests. Please slow down."},
                    headers={
                        "Retry-After": "10",
                        "X-RateLimit-Limit": str(self.GENERAL_LIMIT),
                        "X-RateLimit-Remaining": "0"
                    }
                )

            self.general_requests[client_ip].append(now)

        # Process request
        response = await call_next(request)
        self._apply_security_headers(response)
        return response

    def _apply_security_headers(self, response: Response):
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
