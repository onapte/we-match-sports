from django.shortcuts import render, redirect
from .services import producer, consumer
from django.http import HttpResponse, JsonResponse
from pymongo.mongo_client import MongoClient
from datetime import datetime
import json
from bson.objectid import ObjectId
from .utils import load_key, encrypt_message, decrypt_message
from wematchsports.logging import log_message

uri = "mongodb+srv://onapte:Mongo12345@cluster0.cxi8r.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(uri)
db = client["wematchsports_db"]

users = db['user']
messages = db['message']
userMessagePairs = db['usermessagepairs']
connections = db['connection']

def test_send_message(request):
    to_email = 'satya@microsoft.com'
    from_email = 'hello@gmail.com'

    from_user = users.find_one({'email': from_email})
    to_user = users.find_one({'email': to_email})

    current_datetime = datetime.now()
    formatted_datetime = current_datetime.strftime('%I:%M %p, %Y-%m-%d')

    new_message = {
        'sender_id': from_user['_id'],
        'receiver_id': to_user['_id'],
        'content': "Hi, Satya! I hope this message finds you well. Yada. Yada.",
        'timestamp': formatted_datetime
    }

    messages.insert_one(new_message)

    log_message(f"Message sent from {from_email} to {to_email} at {formatted_datetime}")

    return JsonResponse({"Status": 200})

def view_chats(request):
    user_email = request.session.get('user_email')
    if not user_email:
        return redirect('auth_service:login')

    user = users.find_one({'email': user_email})
    sent_messages = messages.find({'sender_id': user['_id']})
    rec_messages = messages.find({'receiver_id': user['_id']})

    key = load_key()

    info_list = {}

    for message in sent_messages:
        receiver_id = message['receiver_id']
        content = decrypt_message(message['content'], key)
        timestamp = message['timestamp']
        message_id = message['_id']

        receiver = users.find_one({'_id': receiver_id})

        if str(receiver_id) not in info_list:
            data = {
                'first_name': receiver['first_name'],
                'last_name': receiver['last_name'],
                'messages': [
                    {
                        'message_id': str(message_id),
                        'type': 'sent',
                        'content': content,
                        'timestamp': timestamp
                    }
                ]
            }

            info_list[str(receiver_id)] = data

        else:
            data = info_list[str(receiver_id)]

            new_message = {
                'message_id': str(message_id),
                'type': 'sent',
                'content': content,
                'timestamp': timestamp
            }

            data['messages'].append(new_message)
            info_list[str(receiver_id)] = data

    for message in rec_messages:
        sender_id = message['sender_id']
        content = decrypt_message(message['content'], key)
        timestamp = message['timestamp']
        message_id = message['_id']

        sender = users.find_one({'_id': sender_id})

        if str(sender_id) not in info_list:
            data = {
                'first_name': sender['first_name'],
                'last_name': sender['last_name'],
                'messages': [
                    {
                        'message_id': str(message_id),
                        'type': 'received',
                        'content': content,
                        'timestamp': timestamp
                    }
                ]
            }

            info_list[str(sender_id)] = data

        else:
            data = info_list[str(sender_id)]

            new_rec_message = {
                'message_id': str(message_id),
                'type': 'received',
                'content': content,
                'timestamp': timestamp
            }

            data['messages'].append(new_rec_message)
            info_list[str(sender_id)] = data

    for obj_id, data in info_list.items():
        data['messages'].sort(
            key=lambda x: datetime.strptime(x['timestamp'], '%I:%M %p, %Y-%m-%d'),
        )

    user_connections_1 = connections.find({"user1_id": user['_id']})
    user_connections_2 = connections.find({"user2_id": user['_id']})

    for connection in user_connections_1:
        if str(connection['user2_id']) not in info_list:
            connected_user = users.find_one({'_id': connection['user2_id']})
            info_list[str(connection['user2_id'])] = {
                'first_name': connected_user['first_name'],
                'last_name': connected_user['last_name'],
                'messages': []
            }
    
    for connection in user_connections_2:
        if str(connection['user1_id']) not in info_list:
            connected_user = users.find_one({'_id': connection['user1_id']})
            info_list[str(connection['user1_id'])] = {
                'first_name': connected_user['first_name'],
                'last_name': connected_user['last_name'],
                'messages': []
            }

    return render(request, 'messaging/home.html', {
        'info_list': info_list
    })

def view_chat(request):
    user_email = request.session.get('user_email')
    if not user_email:
        return redirect('auth_service:login')

    return render(request, 'messaging/viewChats.html')

def send_message(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        message_content = data.get('message-content')

        key = load_key()
        encrypted_content = encrypt_message(message_content, key)

        current_datetime = datetime.now()
        formatted_datetime = current_datetime.strftime('%I:%M %p, %Y-%m-%d')

        user_id = data.get('user_id')
        current_user_email = request.session.get('user_email')
        current_user = users.find_one({'email': current_user_email})
        current_user_id = str(current_user['_id'])

        log_message(f"Sending message from {current_user_email} to user ID: {user_id}")

        chat_producer = producer.create_new_producer()
        producer.send_message(chat_producer, current_user_id, user_id, encrypted_content)

        latest_msg = consumer.receive_message(user_id)

        new_message = {
            'sender_id': ObjectId(str(latest_msg['sender_id'])),
            'receiver_id': ObjectId(str(latest_msg['recipient_id'])),
            'content': latest_msg['content'],
            'timestamp': formatted_datetime
        }

        log_message(f"New message created: {new_message}")

        messages.insert_one(new_message)

        return JsonResponse({}, status=200)
    
    return JsonResponse({}, status=404)

def get_user_messages(request, user_id):
    if request.method == 'GET':
        user = users.find_one({'_id': ObjectId(user_id)})
        current_user_email = request.session.get('user_email')
        current_user = users.find_one({'email': current_user_email})

        messages_to_user = messages.find({'sender_id': current_user['_id'], 'receiver_id': user['_id']})
        messages_to_currUser = messages.find({'sender_id': user['_id'], 'receiver_id': current_user['_id']})

        key = load_key()

        messages_list = []
        for message in messages_to_user:
            message_data = {
                'message_id': str(message['_id']),
                'type': 'sent',
                'content': decrypt_message(message['content'], key),
                'timestamp': message['timestamp']
            }

            messages_list.append(message_data)

        for message in messages_to_currUser:
            message_data = {
                'message_id': str(message['_id']),
                'type': 'received',
                'content': decrypt_message(message['content'], key),
                'timestamp': message['timestamp']
            }

            messages_list.append(message_data)

        messages_list.sort(
            key=lambda x: datetime.strptime(x['timestamp'], '%I:%M %p, %Y-%m-%d'),
        )

        data = {
            '_id': user_id,
            'first_name': user['first_name'],
            'last_name': user['last_name'],
            'messages': messages_list
        }

        log_message(f"User messages retrieved for user ID: {user_id}")

        return JsonResponse(data)
    
    return JsonResponse({'error': 'Invalid request!'}, status=400)
