from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from hashlib import sha256
from django.contrib import messages
from pymongo import MongoClient
from django.urls import reverse
from wematchsports.logging import log_message

uri = "mongodb+srv://onapte:Mongo12345@cluster0.cxi8r.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(uri)
db = client["wematchsports_db"]
collection = db["user"]

def error_view(request, ignored):
    context = {
        "message": "Page not found."
    }
    return render(request, 'authentication/error.html', context)


def login_view(request):
    log_message("Login view accessed.")
    if request.method == 'POST':
        log_message("Processing login POST request.")
        email = request.POST.get('email')
        password = request.POST.get('password')
        log_message(f"User attempting to log in with email: {email}")

        user = collection.find_one({"email": email})
        
        if not user:
            log_message("Login failed: Invalid email.")
            context = {
                "message":"Invalid email or password. Please try again."
            }
            return render(request, 'authentication/error.html', context)

        hashed_password = sha256(password.encode()).hexdigest()
        log_message("Password hashed for comparison.")

        if hashed_password != user.get("password"):
            log_message("Login failed: Password mismatch.")
            context = {
                "message":"Invalid email or password. Please try again."
            }
            return render(request, 'authentication/error.html', context)
        
        request.session['user_email'] = user['email']
        log_message(f"Login successful for email: {email}")
        
        return redirect('general:dashboard')
    return render(request, 'authentication/login.html')


def sign_up_view(request):
    log_message("Signup view accessed.")
    if request.method == 'POST':
        log_message("Processing signup POST request.")
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        city = request.POST.get('city')
        country = request.POST.get('country')
        age = request.POST.get('age')
        game_1 = request.POST.get('game_1')
        game_2 = request.POST.get('game_2')
        log_message(f"Signup details received for email: {email}")

        existing_user = collection.find_one({"email": email})
        if existing_user:
            log_message("Signup failed: Email already registered.")
            messages.error(request, "Email is already registered.")
            return redirect('auth_service:signup')

        if password != confirm_password:
            log_message("Signup failed: Passwords do not match.")
            messages.error(request, "Passwords do not match.")
            return redirect('auth_service:signup')

        hashed_password = sha256(password.encode()).hexdigest()
        log_message("Password hashed for storage.")

        user_data = {
            "email": email,
            "password": hashed_password,
            "first_name": fname,
            "last_name": lname,
            "city": city,
            "country": country,
            "age": age,
            "game_1": game_1,
            "game_2": game_2
        }

        collection.insert_one(user_data)
        log_message(f"New user registered with email: {email}")

        messages.success(request, "Account created successfully. Please log in.")
        return redirect('auth_service:login')

    return render(request, 'authentication/sign_up.html')

def logout_view(request):
    log_message("Logout view accessed.")
    request.session.flush()
    log_message("User session cleared.")
    return redirect(reverse('auth_service:login'))
