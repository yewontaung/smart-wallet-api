from pwdlib import PasswordHash


password_hasher = PasswordHash.recommended()

def hash_password(password:str) -> str:
    return password_hasher.hash(password)

def verify_password(password, hashed_password) -> bool:
    return password_hasher.verify(password, hashed_password)