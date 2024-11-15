import json
import jwt
import bcrypt
from uuid import uuid4
from typing import Optional
from picture_chat.repositories.user_repository import UserRepository
from picture_chat.entities.user import User
from picture_chat.config import Config
from datetime import datetime, timedelta


def encrypt_password(password: str) -> bytes:
    password_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hash = bcrypt.hashpw(password_bytes, salt)
    return hash.decode('utf-8')


def get_expiration_date() -> str:
    return str(round((datetime.now() + timedelta(days=7)).timestamp()))


def get_new_token(username: str, password: str) -> Optional[str]:
    user_repository = UserRepository()
    user = user_repository.verify_user_credentials(username, password)
    if not user:
        return None
    return jwt.encode(
        {
            "username": username,
            "uuid": str(user.uuid),
            "exp": get_expiration_date()
        },
        Config().secret_key,
        algorithm="HS256"
    )


def extends_token(token: str) -> Optional[str]:
    try:
        new_token = json.loads(jwt.decode(token, Config().secret_key, algorithms="HS256"))
        new_token['exp'] = get_expiration_date()
        return jwt.encode(
            new_token,
            Config().secret_key,
            algorithm="HS256"
        )
    except jwt.exceptions.DecodeError as e:
        print(e)
        return None


def register(name: str, password: str) -> User:
    user_repository = UserRepository()
    encrypted_password = encrypt_password(password)
    user = User(
        uuid=uuid4(),
        name=name
    )
    user_repository.create_new_user(user, encrypted_password)
    return user


def authenticate(token: bytes) -> bool:
    try:
        jwt.decode(token, Config().secret_key, algorithms="HS256")
        return True
    except jwt.exceptions.DecodeError:
        return False
    except jwt.exceptions.ExpiredSignatureError:
        return False
