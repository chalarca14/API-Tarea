import hashlib
import secrets

def hash_password(password: str) -> str:
    """Genera un hash SHA-256 para la contraseña."""
    return hashlib.sha256(password.encode("utf-8")).hexdigest()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica si la contraseña ingresada coincide con el hash almacenado."""
    return hash_password(plain_password) == hashed_password

def generate_token() -> str:
    """Genera un token de sesión aleatorio seguro."""
    return secrets.token_hex(20)

