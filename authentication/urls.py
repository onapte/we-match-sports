from django.urls import path
from . import views

app_name = 'auth_service'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('signup/', views.sign_up_view, name='signup'),
    path('logout/', views.logout_view, name='logout'),
]