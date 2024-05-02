import os
import requests
from dotenv import load_dotenv

from django.forms import ValidationError

from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes

from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication

from .serializers import CharacterSerializer, CharacterIdSerializer, RegisterSerializer
from .models import Character
from .utils.get_character_by_id import get_character

load_dotenv()
one_api_key = os.environ.get("ONE_API_KEY")


class RegisterUser(CreateAPIView):
    """
    API view for registering a new user. 
    CreateAPIView is generic view that provides a `post` method to create a new object.

    Usage:
    - Send a POST request with the `username` and `password` in the request data.
    - The `username` must be unique.
    - If the data is successfully validated, a new user is created.
    - Returns a success message if the operation is successful.

    Exceptions:
    - If the data fails validation (e.g., missing required fields), a 400 Bad Request response is returned.
    """
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "code": "success",
                    "message": "User created successfully.",
                }
            )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetCharacter(APIView):
    """
    API view for fetching character data by ID.

    Usage:
    - Send a GET request with the `character_id` in the URL.
    - The `character_id` corresponds to the unique identifier of the character.
    - If the character data is successfully fetched, it is returned in the response.

    Exceptions:
    - If there is an error fetching character data (e.g., invalid ID or network issues), a 400 Bad Request response is returned.
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class = CharacterSerializer

    def get(self, request, character_id):
        try:
            character_data = get_character(character_id, one_api_key)
            character_data = character_data['docs'][0]
            
            return Response(character_data)
        
        except requests.exceptions.HTTPError as e:
            return Response({"error": "Character not found"}, status=status.HTTP_404_NOT_FOUND)
        
        except requests.exceptions.RequestException as e:
            return Response({"error": "Error fetching character data"}, status=status.HTTP_400_BAD_REQUEST)


class AddFavoriteCharacter(APIView):
    """
    API view for adding a character to the user's favorites.

    Requires authentication via JWT token.

    Usage:
    - Send a POST request with the `character_id` in the request data.
    - The `character_id` corresponds to the unique identifier of the character.
    - If the character data is successfully fetched and validated, it is added to the user's favorites.
    - Returns a success message if the operation is successful.

    Exceptions:
    - If there is an error fetching character data (e.g., invalid ID or network issues), a 400 Bad Request response is returned.
    - If the character data fails validation (e.g., missing required fields), a 400 Bad Request response is returned.
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class = CharacterSerializer
    character_id_serializer = CharacterIdSerializer

    @extend_schema(        
        request=character_id_serializer,
        responses=serializer_class
    )
    
    def post(self, request):
        character_id = request.data.get("character_id")

        try:
            character_data = get_character(character_id, one_api_key)
            character_data = character_data['docs'][0]
            character_data['user'] = request.user.id

            serializer = CharacterSerializer(data=character_data)
            serializer.is_valid(raise_exception=True)
            
            if Character.objects.filter(user=request.user, _id=character_id).exists():
                return Response({"error": "Character already exists in favorites."}, status=status.HTTP_400_BAD_REQUEST)
            
            else:
                serializer.save()
            
            return Response(
                {
                    "code": "success",
                    "message": "Character added to favorites.",
                }
            )
        
        except requests.exceptions.RequestException as e:
            return Response({"error": "Error fetching character data"}, status=status.HTTP_400_BAD_REQUEST)
        
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class ListFavoriteCharacters(APIView):
    """
    API view for listing favorite characters associated with the authenticated user.

    Requires authentication via JWT token.

    Usage:
    - Send a GET request to retrieve a list of characters favorited by the user.
    - Returns a serialized representation of the favorite characters.

    Exceptions:
    - If no favorite characters are found for the user, a 404 Not Found response is returned.
    """

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    serializer_class = CharacterSerializer

    def get(self, request):
        try:
            characters = Character.objects.filter(user=request.user)
            
            if characters.exists():
                serializer = CharacterSerializer(characters, many=True)
                return Response(serializer.data)
            
            else:
                return Response({"message": "No favorite characters."}, status=status.HTTP_404_NOT_FOUND)
        
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
