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
import hashlib
from fastapi import Header, HTTPException, status

from .config import get_settings

ANONYMOUS_CLIENT = "anonymous"
SCHEME = "Bearer"


def verify_bearer_token(
    authorization: str | None = Header(default=None),
    x_client_id: str | None = Header(default=None),
) -> str:

    print(
        "AUTH ENTRY:",
        "present=", authorization is not None,
        "length=", len(authorization or ""),
        "starts_bearer=", (authorization or "").lower().startswith("bearer "),
        flush=True,
    )

    if not authorization:
        print("AUTH FAIL: missing authorization", flush=True)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="invalid or missing bearer token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    scheme, _, token = authorization.partition(" ")

    print(
        "AUTH PARSED:",
        "scheme=", scheme,
        "token_len=", len(token),
        flush=True,
    )

    if scheme.lower() != "bearer" or not token:
        print("AUTH FAIL: bad scheme or empty token", flush=True)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="invalid or missing bearer token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    expected_token = get_settings().api_token

    print(
        "AUTH COMPARE:",
        "received_len=", len(token),
        "expected_len=", len(expected_token),
        "received_hash=", hashlib.sha256(token.encode()).hexdigest()[:8],
        "expected_hash=", hashlib.sha256(expected_token.encode()).hexdigest()[:8],
        flush=True,
    )

    if not secrets.compare_digest(token, expected_token):
        print("AUTH FAIL: token mismatch", flush=True)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="invalid or missing bearer token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    print("AUTH SUCCESS", flush=True)

    return x_client_id if x_client_id else ANONYMOUS_CLIENT