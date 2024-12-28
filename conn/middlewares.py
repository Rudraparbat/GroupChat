from channels.middleware import BaseMiddleware
from django.shortcuts import render , redirect , HttpResponse
from datetime import datetime ,time
import jwt
class JWTmiddleware(BaseMiddleware) :
    async def  __call__(self , scope , recieve , send) :
        cookies = scope['headers']
        decode_cookie = cookies.decode('utf-8')
        print(decode_cookie)
        try :
            cookies = dict(item.split('=') for item in decode_cookie.split('; '))
            access_token = cookies.get('access_token')
        except :
            access_token  = None
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
            server_time = datetime.utcnow().astimezone().timestamp()
            if access_token :
                data_got_from_token = self.decoder(access_token)
                print(data_got_from_token['exp'])
                print(server_time)
                if data_got_from_token['exp'] < server_time :
                    result =  redirect('/')
                    result.delete_cookie('access_token')
                    result.delete_cookie('refresh_token')
                    return result 
        except :
            print("kyu naahi ho rahi parahi")
    
        return self.response(request)
    def decoder(self , token) :
        decoded_token = jwt.decode(token, options={"verify_signature": False})
        return decoded_token 

