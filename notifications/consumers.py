import json
import datetime as dt
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from asgiref.sync import sync_to_async
from portal.models import *
from django.contrib.auth.models import User
from django.forms.models import model_to_dict as mdt


class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        
        # self.user = self.scope['user'] 
        self.id = await(self.get_id())
        self.projectid = await(self.get_pid())
        self.group = await(self.get_groups())

        # Join room group
        if self.group == "Coordinator":
            await self.channel_layer.group_add(
                'general',
                self.channel_name
                )
            
            await self.channel_layer.group_add(
                'coordinator', 
                self.channel_name
                )
            
            await self.channel_layer.group_add(
                'supervisors',
                self.channel_name
                )
            
            await self.channel_layer.group_add(
                'supervisor' + self.id,
                self.channel_name
                )
            await self.accept()
        
        elif self.group == 'Supervisor':
            await self.channel_layer.group_add(
                'general',
                self.channel_name
            )
          
            await self.channel_layer.group_add(
                'supervisors',
                self.channel_name
            )      
            await self.channel_layer.group_add(
                'supervisor' + self.id,
                self.channel_name
            )
            
            await self.accept()
            
        elif self.group == 'Student':
            
            await self.channel_layer.group_add(
                'general',
                self.channel_name
            ),
            
            await self.channel_layer.group_add(
                'project_group'+ self.projectid,
                self.channel_name
            ),  
            await self.channel_layer.group_add(
                'student' + self.id,
                self.channel_name
            )
            
            await self.accept()
        else:
            await self.close()
    async def disconnect(self, close_code):
        # Leave room group
        #await self.channel_layer.group_discard(self.room_group_name, self.channel_name)
        if self.group == "Coordinator":
            # await self.channel_layer.group_discard(
            #     'general',
            #     self.channel_name
            #     )
            
            await self.channel_layer.group_discard(
                'coordinator',
                self.channel_name
                )
            
            await self.channel_layer.group_discard(
                'supervisors',
                self.channel_name
                )
            
            await self.channel_layer.group_discard(
                'supervisor' + self.id,
                self.channel_name
                )
            
        
        elif self.group == 'Supervisor':
            await self.channel_layer.group_discard(
                'general',
                self.channel_name
            )
          
            await self.channel_layer.group_discard(
                'supervisors',
                self.channel_name
            )
            
            
            await self.channel_layer.group_discard(
                'supervisor' + self.id,
                self.channel_name
            )
            
            
        elif self.group == 'Student':
            
            await self.channel_layer.group_discard(
                'general',
                self.channel_name
            ),
            
            await self.channel_layer.group_discard(
                'students',
                self.channel_name
            ),
            
            await self.channel_layer.group_discard(
                'project_group'+self.projectid,
                self.channel_name
            ),  
            await self.channel_layer.group_discard(
                'student' + self.id,
                self.channel_name
            )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        await (self.mark_as_read(text_data_json['notification_id']))

    async def send_notifications(self, event):
         
        sender = event ['sender']
        message = event['message']
        stype = event ['notiftype']
        
        if stype == 'Student':
            sender_name = await(self.get_full_name(sender, 'Student'))
        elif stype == 'Supervisor':
            sender_name = await(self.get_full_name(sender, 'Supervisor'))
            
        sender_img = event['senderimg']
        

        # await self.save_gen_message(send_user,message,receiver)
        
        await self.send(text_data=json.dumps({
        'sender': sender_name,
        'message' :str(message),
        'image': sender_img,
        # 'date' : dt.datetime.now
    })) 
        
    @database_sync_to_async  
    def get_groups(self):
        return str(self.scope['user'].groups.all().first())

    @database_sync_to_async
    def get_id(self):
        if str(self.scope['user'].groups.all().first()) == 'Coordinator':
            return str(self.scope['user'].supervisor.id)
        elif str(self.scope['user'].groups.all().first()) == 'Supervisor':
            return str(self.scope['user'].supervisor.id)
        elif str(self.scope['user'].groups.all().first()) == 'Student':
            return str(self.scope['user'].student.id)
            
    @database_sync_to_async   
    def get_pid(self):
        try:
            return str(self.scope['user'].student.project.id)
        except Exception:
            return 'None'
        
    
    @database_sync_to_async   
    def mark_as_read(self,sid):
        unread = Notifications.objects.filter(receiver_id=int(sid)).filter(read = False)
        for notification in unread:
            notification.read = True
            notification.save()
        return unread

    
    @database_sync_to_async  
    def get_full_name(self, idi, user_type):
        if user_type == 'Student':
            user = User.objects.get(id=idi)
            return str(user.student.first_name + ' ' + user.student.last_name)
        if user_type == 'Supervisor':
            user = Supervisor.objects.get(user_id = idi)
            return str(user.first_name + ' ' + user.other_names)
        
        


class ChatConsumer(AsyncWebsocketConsumer):
    
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        
        
        await self.channel_layer.group_add(
           self.room_group_name,
            self.channel_name
        )

        await self.accept()
    async def disconnect(self, close_code):  
        await self.channel_layer.group_discard(
                self.room_group_name,
                self.channel_name
            ) 
        
    # Receive message from WebSocket
    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']
        senderFname= data['sender_first_name']
        senderLname = data['sender_last_name']
        senderImg = data['sender_img']
        username = data['username']
        project_id = data['project-id']
        
        await self.save_message(username, project_id, message)
        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender' :str(senderFname + ' ' + senderLname),
                'senderimg':  str(senderImg)
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        sender = event['sender']
        message = event['message']
        senderimg = event['senderimg']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'sender' : sender,
            'senderimg' : senderimg
        }))

    @database_sync_to_async   
    def get_pid(self):
        try:
            return str(self.scope['user'].student.project.id)
        except Exception:
            return str(self.scope['user'].supervisor.project.id)
        
    @sync_to_async
    def save_message(self, username, project_id, message):
        user = User.objects.get(username=username)
        project = Project.objects.get(id = project_id)
        ChatMessage.objects.create(sender = user, project = project, message = message)
    