from channels.middleware import BaseMiddleware
from django.shortcuts import render , redirect , HttpResponse
from datetime import datetime ,time
import jwt



    
class JWTmiddleware(BaseMiddleware) :
    async def __call__(self, scope, receive, send):
        # Extract cookies from headers
        access_token = self.extract_access_token(scope['headers'])
        print("Access Token:", access_token)
        if access_token :
            token_data = self.decoder(access_token)
            scope['user'] ={
                'id' : token_data['user_id'],
                'username' : token_data['username']
            }
        print(scope['user'])
        return await super().__call__(scope , receive , send)
    
    def extract_access_token(self, headers):
        # Convert headers list to dict
        headers_dict = dict(headers)
        
        # Get cookie header and decode it
        cookie_header = headers_dict.get(b'cookie', b'').decode('utf-8')
        if not cookie_header:
            print("No cookie header found")
            return None
        
        # Parse cookie string to find access_token
        for cookie in cookie_header.split('; '):
            if cookie.startswith('access_token='):
                return cookie.split('=', 1)[1]  # Split on first '=' only
        
        print("No access_token in cookies")
        return None
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



