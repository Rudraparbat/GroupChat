import uuid
import bcrypt
from rest_framework_simplejwt.tokens import RefreshToken
import jwt
from .views import *
class PasswordGenerator :
    def generate() :
        return str(uuid.uuid4().hex)[:8]
    def chat_id_generate() :
        return str(uuid.uuid4().hex)
    def salt_hash_generator(password) :
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed_password
    def check_password(password , hashed_password) :
        if bcrypt.checkpw(password , hashed_password.encode('utf-8')) :
            return True
        else :
            return False
    def decode_token(token) :
        decoded_token = jwt.decode(token, options={"verify_signature": False})
        return decoded_token 


class Myrefreshtoken(RefreshToken) :
    @classmethod
    def for_user(self , user) :
        token = super().for_user(user)
        token['id'] = user.id
        token['username'] = user.username
        return token
