from channels.generic.websocket import AsyncWebsocketConsumer
import json
from django.core.cache import cache
from channels.layers import get_channel_layer
import redis
import os
from urllib.parse import urlparse

#  Redis setup

REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379/0")
parsed_url = urlparse(REDIS_URL)
redis_client = redis.StrictRedis(
    host=parsed_url.hostname,
    port=parsed_url.port,
    db=int(parsed_url.path.lstrip('/')) if parsed_url.path else 0, 
    password=parsed_url.password, 
    ssl=False  
)

class Chatapp(AsyncWebsocketConsumer) :
    async def connect(self) :
        group_name = self.scope['url_route']['kwargs']['room_name']
        group_id = self.scope['url_route']['kwargs']['room_id']
        self.room_group_name = f'Chat_{group_name}_{group_id}'
        self.redis_key = self.room_group_name
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()
        # shows last 20 messages..
        if self.redis_key :
            latest_messages = redis_client.lrange(self.redis_key , -20 , -1)
            if latest_messages :
                await self.send(json.dumps({
                    "type" : "old_message",
                    'messages': list(map(lambda msg: json.loads(msg.decode()), latest_messages))
                }))
                print(list(map(lambda msg: json.loads(msg.decode()), latest_messages)))





    async def receive(self, text_data=None, bytes_data=None):
        if text_data :
            data_got = json.loads(text_data)
            await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type' : 'chat_message',
                        "username" : data_got['username'],
                        "message" : data_got['message']
                    }
                )
            print("message :",data_got['message'])
            if data_got['type'] == "new_message" :
                redis_client.rpush(self.redis_key,json.dumps({
                    "username" : data_got['username'],
                    "message" : data_got['message']
                }))
            redis_client.expire(self.redis_key,86400) 
        else :
            print("its byte code")



    async def chat_message(self, event) :
        data = event['message']
        await self.send(text_data=json.dumps({
                    "type" : "new_message",
                    "message" : data,
                    "username" : event['username']
            }))


    # async def show_user_count(self):
    #     channel_layer = get_channel_layer()
    #     group_channels = await channel_layer.group_channels(self.room_group_name)
    #     user_count = len(group_channels)
    #     await self.channel_layer.group_send(
    #         self.room_group_name,
    #         { 
    #             "type" : "Joined_users",
    #             "user_count" : user_count
    #         }
    #     )

    # async def Joined_users(self , event) :
    #     data = event['user_count']
    #     await self.send(json.dumps({
    #         "type" : "joined",
    #         "users" : data
    #     }))

    
    async def disconnect(self , close_code) :
        await self.channel_layer.group_discard(
            self.room_group_name, 
            self.channel_name
        )
        print("connection ended")