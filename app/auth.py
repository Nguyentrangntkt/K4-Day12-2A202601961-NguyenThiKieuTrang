"""CP3 — Xác thực bằng Bearer token.

Public URL = ai cũng gọi được. Không có lớp này, hóa đơn LLM của bạn do
người lạ quyết định.

Chuẩn dùng ở đây là **RFC 6750** — token đi trong header ``Authorization``:

    Authorization: Bearer <token>

Đây là cách mọi API lớn (GitHub, Stripe, OpenAI) nhận token, nên client viết
bằng ngôn ngữ nào cũng có sẵn thư viện hiểu nó.
"""

from __future__ import annotations

import secrets
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi import Depends
from fastapi import Header, HTTPException, status

from .config import get_settings

ANONYMOUS_CLIENT = "anonymous"
SCHEME = "Bearer"
bearer_scheme = HTTPBearer(auto_error=False)

def verify_bearer_token(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
    x_client_id: str | None = Header(default=None),
) -> str:
    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="invalid or missing bearer token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if credentials.scheme.lower() != "bearer" or not credentials.credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="invalid or missing bearer token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = credentials.credentials
    expected_token = get_settings().api_token

    if not secrets.compare_digest(token, expected_token):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="invalid or missing bearer token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return x_client_id if x_client_id else ANONYMOUS_CLIENT