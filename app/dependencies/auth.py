from typing import Annotated
from fastapi import HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from ..config.config import Settings, get_settings

# Use oauth2_scheme to extract the token from the header
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="")
ALGORITHM = "HS256"


# Class for the extracted token payload
class TokenPayload:
    def __init__(self, userId, username):
        self.user_id = userId
        self.username = username


async def get_auth_token_header(
    auth_token: Annotated[str, Depends(oauth2_scheme)],
    settings: Annotated[Settings, Depends(get_settings)],
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        # Decode the token and extract the payload
        decoded_token = jwt.decode(
            auth_token, settings.jwt_secret, algorithms=[ALGORITHM]
        )
        token_payload_data: dict = decoded_token.get("tokenPayload")
        token_payload = TokenPayload(**token_payload_data)

        # Check the token payload
        if token_payload is None or token_payload.user_id is None:
            raise credentials_exception

        # token_data = TokenData(user_id=user_id)
    except JWTError:
        raise credentials_exception
    except Exception as e:
        print(f"An error occurred: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    # return user_id
