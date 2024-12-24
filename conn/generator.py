import uuid
from .views import *
class PasswordGenerator() :
    def generate() :
        return str(uuid.uuid4().hex)[:8]
    def chat_id_generate() :
        return str(uuid.uuid4().hex)
