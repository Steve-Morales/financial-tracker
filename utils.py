from flask_bcrypt import Bcrypt
from database import db

app = None
bcrypt = Bcrypt(app)


def hash_password(password):
    return bcrypt.generate_password_hash(password).decode('utf-8') # use decode if need a string


def password_match(password):
    p_hash = hash_password(password)
    return bcrypt.check_password_hash(p_hash, password)
