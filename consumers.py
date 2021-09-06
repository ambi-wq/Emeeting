# chat/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer
room_group_array = []
refreshpresentation = []
class ChatConsumer(AsyncWebsocketConsumer):
    path_remaining = ''
    room_group_name_pre = ''
    room_group_name = ''
    async def connect(self):
        self.path_remaining = self.scope['path_remaining']
        #print("path--->",self.path_remaining)

        # self.room_name = self.scope['url_route']['kwargs']['room_name']
        # self.room_group_name = 'chat_%s' % self.room_name
        # # self.channel_name = self.channel_name + self.room_group_name + self.path_remaining
        # print("global--->", self.channel_name, '\n grpname---->', self.room_group_name)


        if self.path_remaining == '/startPresentation' or self.path_remaining =='refreshpresentation':
            self.room_name = self.scope['url_route']['kwargs']['room_name']
            self.room_group_name = 'chat_p_%s' % self.room_name
            self.room_group_name_pre = 'chat_%s' % self.room_name
            #self.channel_name = self.channel_name + self.room_group_name + '_startPresentation'
            print("inside startPresentation--->", self.channel_name, '\n grpname---->', self.room_group_name)
        else:
            self.room_name = self.scope['url_route']['kwargs']['room_name']
            self.room_group_name = 'chat_p_%s' % self.room_name
            self.room_group_name_pre = 'chat_%s' % self.room_name
            print("startgrp--->", self.channel_name, '\n grpname---->', self.room_group_name)

        #
         #   self.room_group_name_pre = 'chat_p_%s' % self.room_name
        #     #self.channel_name_pre = self.channel_name + self.room_group_name_pre + '_startPresentation'
        #     # print("nonadmin start pres consumer room--->", self.channel_name, '||', self.room_group_name)

        # Join room group
        await self.channel_layer.group_add(
                self.room_group_name_pre,
                self.channel_name
        )
        await self.accept()


        # if self.path_remaining == '/startPresentation' or self.path_remaining == 'refreshPresentation':
        #     await self.channel_layer.group_add(
        #         self.room_group_name,
        #         self.channel_name
        #     )
        #     await self.accept()
        # else:
        #     await self.channel_layer.group_add(
        #         self.room_group_name,
        #         self.channel_name
        #     )
        #
        #     await self.channel_layer.group_add(
        #         self.room_group_name_pre,
        #         self.channel_name
        #     )
        #     await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        print("Leave Group:",self.room_group_name)
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )


    # Receive message from WebSocket
    async def receive(self, text_data):
        #print("path remaining---->",self.path_remaining)
        print("room_group_array_______", room_group_array)
        print("consumer recieve--->",text_data)
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        servicename = text_data_json['servicename']

        if servicename == 'startpresentation':
            print("pres room group---->",self.room_group_name_pre)
            # Send message to room group
            # await self.channel_layer.group_send(
            #
            #         self.room_group_name,
            #         {
            #             'type': 'chat_message',
            #             'message': message,
            #             'servicename': servicename
            #         }
            # )
            await self.channel_layer.group_send(

                self.room_group_name_pre,
                {
                    'type': 'chat_message',
                    'message': message,
                    'servicename': servicename
                }
            )
            s = {self.room_group_name_pre: text_data, "Channel_name": self.channel_name,"prev group":self.room_group_name_pre}
            room_group_array.append(s)

        elif servicename == 'refreshpresentation' :
            print("refresh room group---->", self.room_group_name_pre)
            print("Refresh prsentation Array-------------->",refreshpresentation)

            await self.channel_layer.group_send(

                self.room_group_name_pre,
                {
                    'type': 'chat_message',
                    'message': message,
                    'servicename': servicename
                }
            )

            r = {'message' : message,'servicename':servicename,'Room':self.room_group_name_pre}
            refreshpresentation.append(r)

            s = {self.room_group_name_pre: text_data, "Channel_name": self.channel_name}
            room_group_array.append(s)

        else:
            print("start room group---->", self.room_group_name_pre)
            await self.channel_layer.group_send(

                self.room_group_name_pre,
                {
                    'type': 'chat_message',
                    'message': message,
                    'servicename': servicename
                }
            )

        # print("start room group---->", self.room_group_name)
        # await self.channel_layer.group_send(
        #
        #     self.room_group_name,
        #     {
        #         'type': 'chat_message',
        #         'message': message,
        #         'servicename':servicename
        #     }
        # )

            #print("admin display--->", self.room_group_name,'------->',message)
            s = {self.room_group_name_pre: text_data,"Channel_name":self.channel_name}
            room_group_array.append(s)

        print("room_group_array  after send_______", room_group_array)
        #print("channel name--->",self.channel_name)

    # Receive message from room group
    async def chat_message(self, event):
        print("event---->",event,"\n websocket channel\ Room name---->",self.channel_name,self.room_group_name_pre)
        message = event['message']
        servicename = event['servicename']

        # Send message to WebSocket
        #print("send to websocket---->",message,"\n websocket channel---->",self.channel_name)
        await self.send(text_data=json.dumps({
            'message': message,
            'servicename':servicename
        }))




