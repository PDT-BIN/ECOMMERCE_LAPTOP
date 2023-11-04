from django.urls import path

from . import views
from controls.views import home_page


urlpatterns = [
    # HOME PAGE.
    path('', home_page, name='home'),
    # SYSTEM FUNCTIONS.
    path('signin/', views.signin_page, name='signin'),
    path('signup/', views.signup_page, name='signup'),
    path('logout/', views.logout_page, name='logout'),
    path('forgot/', views.forgot_page, name='forgot'),
    # TOKEN ACTIVATION.
    path('activate/<uidb64>/<token>', views.activate, name='activate'),
    path('reset/<uidb64>/<token>', views.reset_password, name='reset'),
    # USER INFORMATION.
    path('profile/<int:choice>', views.profile_page, name='profile'),
    path('update-profile/', views.update_profile, name='update-profile'),
    path('change-password/', views.change_password, name='change-password'),
    path('manage-address/', views.create_or_update_address, name='manage-address'),
    path('delete-address/', views.delete_address, name='delete-address'),
    # CHATBOT.
    path('chatting/', views.chatting, name='chatting'),
    path('getChat/', views.getChat, name='getChat'),
    path('thumbsup/', views.thumbsup, name='thumbsup'),
    path('thumbsdown/', views.thumbsdown, name='thumbsdown'),
]
