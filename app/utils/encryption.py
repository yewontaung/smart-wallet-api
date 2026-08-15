from typing import Any

import jwt

from app.utils import env


def encode_jwt(payload:dict[str, Any]):
    return jwt.encode(payload, env.JWT_SECRET, env.ALGO)

def decode_jwt(token:str) -> dict[str, Any]:
    return jwt.decode(token, env.JWT_SECRET, env.ALGO)