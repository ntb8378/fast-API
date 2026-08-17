import bcrypt

def hash_password(password: str, cost_factor: int = 12) -> str:
    password_byte = password. encode("utf-8")
    salt = bcrypt.gensalt(rounds = cost_factor)
    hash_password = bcrypt.hashpw(password_byte, salt)
    return hash_password.decode("utf-8")