from django.urls import path
from core import views

urlpatterns = [
    path('signup/', views.SignupView.as_view()),
    path('login/', views.LoginView.as_view()),
    path('token/', views.GenerateTokenView.as_view()),
    path('send_message/', views.CreateMessageView.as_view()),
    path('messages/', views.ListMessageView.as_view())
]