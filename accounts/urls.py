from django.urls import path
from . import views

urlpatterns = [
    path("register/", views.register, name="register"),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('dashobard/', views.dashobard, name='dashobard'),
    path('add-amount/', views.add_amount, name='add_amount'),
    path('change_password/', views.change_password, name='change_password'),
    # path('borrowed_books/', views.borrowed_books, name='borrowed_books'),
    # path('borrowed_books/', views.add_amount, name='add_amount'),
]
