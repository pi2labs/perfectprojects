from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.loginUser, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('register/', views.registerUser, name='register'),


    path('', views.profiles, name='profiles'),
    path('profile/<str:pk>', views.userProfile, name='user_profile'),
    path('account/', views.userAccount, name='account'),
    path('edit-account/', views.editUserAccount, name='edit'),

    path('create-skill/', views.createSkill, name='create_skill'),
    path('update-skill/<str:pk>', views.updateSkill, name='update_skill'),
    path('delete-skill/<str:pk>', views.deleteSkill, name='delete_skill'),

    path('inbox/', views.inbox, name='inbox'),
    path('message/<str:pk>', views.viewMessage, name='message'),
    path('send-message/<str:pk>/', views.createMessage, name='send_message'),

]
