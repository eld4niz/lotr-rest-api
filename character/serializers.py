from .models import Character
from django.contrib.auth.models import User
from rest_framework import serializers

# use get user model
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["username", "password"]

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            password=validated_data["password"]
        )

        return user


class CharacterIdSerializer(serializers.Serializer):
    # we don't need to create a model for this serializer
    
    character_id = serializers.CharField()

    def validate_character_id(self, value):
        try:
            str(value)
        except ValueError:
            raise serializers.ValidationError("Character ID must be an integer.")

        return value

class CharacterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Character
        fields = "__all__"