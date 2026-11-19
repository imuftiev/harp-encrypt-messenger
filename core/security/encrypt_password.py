from pwdlib import PasswordHash


def get_hashed_password(password_hash: PasswordHash, password: str) -> str:
    return password_hash.hash(password)


def verify_hashed_password(password_hash: PasswordHash, plain_password: str, hashed_password: str) -> bool:
    return password_hash.verify(plain_password, hashed_password)
