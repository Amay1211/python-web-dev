from passlib.context import CryptContext
passwordContext = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hashPassword(password: str):
    return passwordContext.hash(password)

def verifyPassword(plainPassword: str, hashedPassword: str):
    return passwordContext.verify(plainPassword, hashedPassword)

