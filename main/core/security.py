import jwt
from jwt.exceptions import InvalidSignatureError
from fastapi import Header, HTTPException, status
from typing import Generator
from main.core.config import Settings

settings = Settings()
async def jwt_required(
    token: str = Header(None),
) -> Generator:
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, \
            detail="Token missing"
        )
    try:
        decoded_jwt = jwt.decode( \
            token, settings.SECRET, algorithms=[settings.JWT_ALGO])
        return decoded_jwt
    except InvalidSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, \
            detail="Invalid Token"
        )
    except Exception as err:
        print("err ", err)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, \
            detail="Invalid Token"
        )
