# import hashlib

# def hash_password(password):
#     return hashlib.sha1(password.encode()).hexdigest()
import bcrypt
class PasswordService:
    ROUNDS = 12
    def hash_password(self, password: str) -> str:
        if not password or not isinstance(password, str):
            raise ValueError("Password must be a non-empty string")
        return bcrypt.hashpw(
            password.encode("utf-8"),
            bcrypt.gensalt(rounds=self.ROUNDS)
        ).decode("utf-8")
    def verify_password(self, raw_password: str, hashed_password: str) -> bool:
        if not raw_password or not hashed_password:
            return False
        return bcrypt.checkpw(
            raw_password.encode("utf-8"),
            hashed_password.encode("utf-8")
        )