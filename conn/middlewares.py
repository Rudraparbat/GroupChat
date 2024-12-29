from channels.middleware import BaseMiddleware
from django.shortcuts import render , redirect , HttpResponse
from datetime import datetime ,time




    
class JWTmiddleware(BaseMiddleware) :
    async def  __call__(self , scope , recieve , send) :
        cookies = scope['headers'][13]
        scopes = scope['headers']
        decode_cookie = cookies[1].decode('utf-8')
        try :
            cookies = dict(item.split('=') for item in decode_cookie.split('; '))
            access_token = cookies.get('access_token')
        except :
            access_token = None
        if access_token :
            token_data = self.decoder(access_token)
            scope['user'] ={
                'id' : token_data['id'],
                'username' : token_data['username']
            }
        return await super().__call__(scope , recieve , send)
    def decoder(self , token) :
        decoded_token = jwt.decode(token, options={"verify_signature": False})
        return decoded_token 

class Tokenvalidation :
    def __init__(self , get_response) :
        self.response = get_response

    def __call__(self , request) :
        try :
            access_token = request.COOKIES.get('access_token')
            refresh_token = request.COOKIES.get('refresh_token')
            server_time = datetime.utcnow().astimezone().timestamp()
            if access_token :
                data_got_from_token = self.decoder(access_token)
                if data_got_from_token['exp'] < server_time:
                    refresh_token_obj = RefreshToken(refresh_token)
                    response = redirect("/")
                    response.delete_cookie("access_token")
                    response.delete_cookie("refresh_token")
                    return response
        except :
            pass
    
        return self.response(request)
    def decoder(self , token) :
        decoded_token = jwt.decode(token, options={"verify_signature": False})
        return decoded_token 



