from django.shortcuts import render, redirect
from django.http import HttpResponse
from hashlib import sha256  # For password hashing
from django.contrib import messages
from pymongo import MongoClient  # Import pymongo to interact with MongoDB
from django.urls import reverse
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from wematchsports.logging import log_message

uri = "mongodb+srv://onapte:Mongo12345@cluster0.cxi8r.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(uri)
db = client["wematchsports_db"]
collection = db["user"]
connections = db["connection"]
connection_reqs = db['connection_request']

def find_matched_players(current_user, players, threshold=0.1):
    """
    Find matched players based on cosine similarity of age and game interests.
    
    Args:
        current_user (dict): The logged-in user's details.
        players (list): List of all players in the database.
        threshold (float): Minimum cosine similarity to consider a match.
        
    Returns:
        list: List of matched players.
    """

    matched_players = []
    
    country_1 = current_user['country']
    city_1 = current_user['city']
    user_game = current_user['game_1'] + " " + current_user['game_2']
    
    log_message(f"Current user: {current_user['email']} - Country: {country_1}, City: {city_1}, Games: {user_game}")

    for player in players:
        if player['email'] == current_user['email']:
            continue
        
        country_2 = player['country']
        log_message(f"Comparing with player - Country: {country_2}")

        vectorizer = TfidfVectorizer()
        tfidf_matrix = vectorizer.fit_transform([country_1, country_2])

        country_similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
        log_message(f"Country similarity: {country_similarity}")

        if country_similarity > 0.6:
            city_2 = player['city']
            log_message(f"Comparing with player - City: {city_2}")

            tfidf_matrix = vectorizer.fit_transform([city_1, city_2])

            city_similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
            log_message(f"City similarity: {city_similarity}")

            if city_similarity > 0.5:
                player_game = player['game_1'] + " " + player['game_2']
                log_message(f"Comparing with player - Games: {player_game}")

                tfidf_matrix = vectorizer.fit_transform([user_game, player_game])

                game_similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
                log_message(f"Game similarity: {game_similarity}")

                if game_similarity > 0.3:
                    matched_players.append(player)
                    log_message(f"Matched player: {player['email']}")

    return matched_players
