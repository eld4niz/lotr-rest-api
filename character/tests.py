from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import AccessToken
from .models import Character

class AddFavoriteCharacterTest(APITestCase):
    def initialize(self):
        self.user = User.objects.create_user(username='test_user', password='test_password')
        
        # Generate a JWT token for the test user
        token = AccessToken.for_user(self.user)
        self.token = str(token)
        
        # Set the JWT token in the test client's credentials
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')


    def test_add_favorite_character_success(self):
        character_id = "5cdbdecb6dc0baeae48cfaa2"
        data = {"character_id": character_id}

        # Send a POST request to add the character to favorites
        response = self.client.post(reverse('favorite-character'), data=data, format='json')
        print(response.data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {"code": "success", "message": "Character added to favorites."})

        # Check if the character is actually added to the user's favorites
        self.assertTrue(Character.objects.filter(user=self.user, _id=character_id).exists())


    def test_add_favorite_character_invalid_id(self):
        character_id = "045690456"  # An invalid character ID for testing
        data = {"character_id": character_id}

        response = self.client.post(reverse('favorite-character'), _id=data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {"error": "Error fetching character data"})


    def test_add_favorite_character_already_exists(self):
        character_id = "5cdbdecb6dc0baeae48cfaa2"
        data = {"character_id": character_id}

        # Add the character to the user's favorites
        Character.objects.create(user=self.user, _id=character_id)

        response = self.client.post(reverse('favorite-character'), data=data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {"error": "Character already exists in favorites."})


class ListFavoriteCharactersTest(APITestCase):
    def initialize(self):
        self.user = User.objects.create_user(username='test_user', password='test_password')
        
        # Generate a JWT token for the test user
        token = AccessToken.for_user(self.user)
        self.token = str(token)
        
        # Set the JWT token in the test client's credentials
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')

        # Add some favorite characters for the test user
        Character.objects.create(user=self.user, _id="5cdbdecb6dc0baeae48cfaa2") # Carcharoth
        Character.objects.create(user=self.user, _id="5cdbdecb6dc0baeae48cfa57") # Huan


    def test_list_favorite_characters(self):
        response = self.client.get(reverse('character-list'))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['_id'], "5cdbdecb6dc0baeae48cfaa2") # Carcharoth
        self.assertEqual(response.data[1]['_id'], "5cdbdecb6dc0baeae48cfa57") # Huan


class GetCharacterFromOneAPITest(APITestCase):
    def initialize(self):
        self.user = User.objects.create_user(username='test_user', password='test_password')
        
        # Generate a JWT token for the test user
        token = AccessToken.for_user(self.user)
        self.token = str(token)
        
        # Set the JWT token in the test client's credentials
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')

        # Add some favorite characters for the test user
        Character.objects.create(user=self.user, _id="5cdbdecb6dc0baeae48cfaa2") # Carcharoth
        Character.objects.create(user=self.user, _id="5cdbdecb6dc0baeae48cfa57") # Huan


    def test_get_character_success(self):
        character_id = "5cdbdecb6dc0baeae48cfaa2"  # Carcharoth

        response = self.client.get(reverse('get-character', kwargs={'character_id': character_id}))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['_id'], character_id)


    def test_get_character_not_found(self):
        character_id = "894568936894365"  # random string

        response = self.client.get(reverse('get-character', kwargs={'character_id': character_id}))

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data, {"error": "Character not found"})