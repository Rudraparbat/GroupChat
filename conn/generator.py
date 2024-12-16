import uuid
class PasswordGenerator() :
    def generate() :
        return str(uuid.uuid4().hex)[:8]