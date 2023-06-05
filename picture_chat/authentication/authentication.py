import jwt
import bcrypt
from uuid import uuid4
from typing import Optional
from picture_chat.repositories.user_repository import UserRepository
from picture_chat.entities.user import User


secret_key = "TO CHANGE IN PRODUCTION"


def encrypt_password(password: str) -> bytes:
    password_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hash = bcrypt.hashpw(password_bytes, salt)
    return hash


def login(username: str, password: str) -> Optional[str]:
    user_repository = UserRepository()
    user = user_repository.verify_user_credentials(username, password)
    if not user:
        return None
    return jwt.encode(
        {
            "username": username,
            "uuid": str(user.uuid)
        },
        secret_key,
        algorithm="HS256"
    )


def register(name: str, password: str) -> User:
    user_repository = UserRepository()
    encrypted_password = encrypt_password(password)
    user = User(
        uuid=uuid4(),
        name=name
    )
    user_repository.create_new_user(user, encrypted_password)
    return user


# TODO handle expirations etc.
def authenticate(token: bytes) -> bool:
    try:
        jwt.decode(token, secret_key, algorithms="HS256")
        return True
    except jwt.exceptions.DecodeError as e:
        print(e)
        return False
