from django.urls import path
from .views import ListFavoriteCharacters, AddFavoriteCharacter, RegisterUser, GetCharacter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    # Auth Endpoints
    path("register/", RegisterUser.as_view(), name="register"),
    path("login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("login/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    
    # Character Endpoints
    path("character/<str:character_id>/", GetCharacter.as_view(), name="get-character"),
    path("character/", AddFavoriteCharacter.as_view(), name="favorite-character"),
    path("list/", ListFavoriteCharacters.as_view(), name="character"),
]