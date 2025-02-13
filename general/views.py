from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from hashlib import sha256
from django.contrib import messages
from pymongo import MongoClient
from pymongo.mongo_client import MongoClient
from matchmaking.views import find_matched_players
from django.views.decorators.cache import cache_control
import json
from bson.objectid import ObjectId
from django.views.decorators.cache import cache_control
from newsapi import NewsApiClient
from wematchsports.logging import log_message

uri = "mongodb+srv://onapte:Mongo12345@cluster0.cxi8r.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(uri)
db = client["wematchsports_db"]
collection = db["user"]
connections = db["connection"]
connection_reqs = db['connection_request']

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def dashboard_view(request):
    log_message("Entering dashboard_view function")

    user_email = request.session.get('user_email')
    if not user_email:
        log_message("User not logged in. Redirecting to login page.")
        return redirect('auth_service:login')

    log_message(f"User email found: {user_email}")

    user = collection.find_one({"email": user_email})
    log_message(f"Fetched user data: {user}")
    context = {
        "email": user.get("email"),
        "first_name": user.get("first_name"),
        "last_name": user.get("last_name"),
        "age": user.get("age"),
        "game_1": user.get("game_1"),
        "game_2": user.get("game_2"),
        "matched_players": None,
    }

    pending_connection_reqs = connection_reqs.count_documents({"receiver_id": user['_id']})
    context["pending_connection_reqs"] = pending_connection_reqs
    log_message(f"Pending connection requests: {pending_connection_reqs}")

    if request.method == 'POST' and 'find_matches' in request.POST:
        log_message("Matchmaking button clicked.")

        players = list(collection.find({}))

        matched_players = find_matched_players(user, players)
        log_message(f"Matched players: {matched_players}")

        for i, matched_player in enumerate(matched_players):
            curr_matched_player = matched_player
            curr_matched_player['id'] = curr_matched_player['_id']
            player_id = curr_matched_player['_id']
            curr_user_id = user['_id']

            c1 = connections.find_one({"user1_id": player_id, "user2_id": curr_user_id})
            c2 = connections.find_one({"user1_id": curr_user_id, "user2_id": player_id})

            if c1 is not None or c2 is not None:
                curr_matched_player['connection_status'] = 'Connected'

            else:
                c1_req = connection_reqs.find_one({"sender_id": curr_user_id, "receiver_id": player_id})
                c2_req = connection_reqs.find_one({"sender_id": player_id, "receiver_id": curr_user_id})

                if c1_req is not None:
                    curr_matched_player['connection_status'] = 'Pending'

                elif c2_req is not None:
                    curr_matched_player['connection_status'] = 'Accept'

                else:
                    curr_matched_player['connection_status'] = 'Not Connected'

            matched_players[i] = curr_matched_player
        context["matched_players"] = matched_players

    log_message("Exiting dashboard_view function")
    return render(request, 'general/dashboard.html', context)

def profile_view(request):
    log_message("Entering profile_view function")

    user_email = request.session.get('user_email')
    if not user_email:
        log_message("User not logged in. Redirecting to login page.")
        return redirect('auth_service:login')

    log_message(f"User email found: {user_email}")

    user = collection.find_one({"email": user_email})
    if not user:
        log_message("User not found in database. Redirecting to login page.")
        return redirect('auth_service:login')

    log_message(f"Fetched user data: {user}")

    if request.method == 'POST' and 'update_profile' in request.POST:
        log_message("Profile update form submitted.")

        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        age = request.POST.get('age')
        city = request.POST.get('city')
        country = request.POST.get('country')
        game_1 = request.POST.get('game_1')
        game_2 = request.POST.get('game_2')

        collection.update_one(
            {"email": user_email},
            {
                "$set": {
                    "first_name": first_name,
                    "last_name": last_name,
                    "age": age,
                    "city": city,
                    "country": country,
                    "game_1": game_1,
                    "game_2": game_2,
                }
            }
        )
        log_message("User profile updated successfully.")

        user = collection.find_one({"email": user_email})

    context = {
        "email": user.get("email"),
        "first_name": user.get("first_name"),
        "last_name": user.get("last_name"),
        "age": user.get("age"),
        "city": user.get("city"),
        "country": user.get("country"),
        "game_1": user.get("game_1"),
        "game_2": user.get("game_2"),
    }
    log_message("Exiting profile_view function")

    return render(request, 'general/profile.html', context)

def connection_request(request):
    log_message("Entering connection_request function")

    user_email = request.session.get('user_email')
    if not user_email:
        log_message("User not logged in. Redirecting to login page.")
        return redirect('auth_service:login')

    if request.method == 'POST':
        log_message("Connection request POST method triggered.")
        user = collection.find_one({'email': user_email})
        sender_id = user['_id']

        data = json.loads(request.body)
        receiver_id = ObjectId(str(data.get('receiver_id')))

        connection_req = {
            'sender_id': sender_id,
            'receiver_id': receiver_id,
            'status': 'Pending'
        }

        connection_reqs.insert_one(connection_req)
        log_message(f"Connection request sent from {sender_id} to {receiver_id}.")
        return JsonResponse({}, status=200)

    if request.method == 'GET':
        log_message("Connection request GET method triggered.")
        user = collection.find_one({'email': user_email})
        user_id = user['_id']

        user_connection_reqs = connection_reqs.find({'receiver_id': user_id})

        data = {}
        for connection_req in user_connection_reqs:
            sender_id = connection_req['sender_id']
            sender = collection.find_one({'_id': ObjectId(str(sender_id))})

            data[sender_id] = {
                'first_name': sender['first_name'],
                'last_name': sender['last_name'],
                'country': sender['country'],
                'age': sender['age'],
                'game_1': sender['game_1'],
                'game_2': sender['game_2']
            }

        log_message("Returning connection requests.")
        return JsonResponse({'data': data}, status=200)

    log_message("Exiting connection_request function")
    return JsonResponse({}, status=400)

def answer_connection_req(request):
    log_message("Entering answer_connection_req function")

    user_email = request.session.get('user_email')
    if not user_email:
        log_message("User not logged in. Redirecting to login page.")
        return redirect('auth_service:login')
    
    if request.method == 'POST':
        log_message("Answer connection request POST method triggered.")
        data = json.loads(request.body)
        action_user_id = ObjectId(str(data.get('action_user_id')))
        verdict = data.get('verdict')

        user = collection.find_one({'email': user_email})
        user_id = user['_id']

        if verdict == 'accepted':
            connection_req = connection_reqs.find_one_and_delete({'sender_id': action_user_id, 'receiver_id': user_id})
            new_connection = {
                'user1_id': user_id,
                'user2_id': action_user_id
            }

            connections.insert_one(new_connection)
            log_message(f"Connection request accepted between {user_id} and {action_user_id}.")

        else:
            connection_req = connection_reqs.find_one_and_delete({'sender_id': action_user_id, 'receiver_id': user_id})
            log_message(f"Connection request declined from {action_user_id}.")

        return JsonResponse({}, status=200)

    log_message("Exiting answer_connection_req function")
    return JsonResponse({}, status=400)

rooms = [
    {'id': 1, 'name': 'American Football'},
    {'id': 2, 'name': 'Soccer'},
    {'id': 3, 'name': 'Tennis'},
    {'id': 4, 'name': 'Cricket'},
    {'id': 5, 'name': 'Basketball'},
    {'id': 6, 'name': 'Table Tennis'},
    {'id': 7, 'name': 'Pickleball'},
    {'id': 8, 'name': 'Billiards'},
]

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def public_rooms(request):
    log_message("Entering public_rooms function")
    log_message(f"Fetched {len(rooms)} public rooms")

    log_message("Rendering public_rooms template")
    return render(request, 'general/public_rooms.html', {'rooms': rooms})

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def room_detail(request, room_name):
    log_message(f"Entering room_detail function for room: {room_name}")

    newsapi = NewsApiClient(api_key='456a4f22e5254311a1cebfccda579d3d')
    log_message(f"NewsApiClient initialized with API key")

    top_headlines = newsapi.get_everything(
        q=room_name,
        language='en',
        sort_by='relevancy',
        page_size=10
    )
    log_message(f"Fetched top headlines for room: {room_name}")

    articles = top_headlines.get('articles', [])
    log_message(f"Extracted {len(articles)} articles")
    
    log_message("Rendering room_detail template")
    return render(request, 'general/room_detail.html', {'room_name': room_name, 'articles': articles})
