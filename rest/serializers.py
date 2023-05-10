from rest_framework.serializers import Serializer, CharField, ModelSerializer, IntegerField, DecimalField
from rest_framework import serializers
from .models import User


class TestObject():
    def __init__(self):
        self.stroka = "Meow"


class BaseUserSerializer(ModelSerializer):
    
    def create(self, validated_data):
        user = User.objects.create_user(
            **validated_data
        )
        return user

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'email', 'country', 'city']
        read_only_fields = ['id']
        extra_kwargs = {'password': {'write_only': True,
                                     'style': {'input_type': 'password'}}, }

class UserSerializer(BaseUserSerializer):
    friend_status = serializers.SerializerMethodField()

    def get_friend_status(self, obj):
        user = self.context['request'].user
        return user.friends.filter(id=obj.id).exists()
    
    class Meta(BaseUserSerializer.Meta):
        fields = BaseUserSerializer.Meta.fields + ['friend_status']

class FriendRequestSerializer(Serializer):
    to_user = serializers.SlugRelatedField(
        queryset=User.objects.all(),
        slug_field='username',
    )

    def validate_to_user(self, value):
        try:
            user_value = User.objects.get(username=value)
        except User.DoesNotExist:
            raise serializers.ValidationError('User does not exist')

        user = self.context['request'].user
        if user.id == user_value.id:
            raise serializers.ValidationError('Cannot send friend request to myself')

        if user.friends.filter(id=user_value.id).exists():
            raise serializers.ValidationError('Users are already friends')
        
        if user.outgoing_friend_requests.filter(id=user_value.id).exists():
            raise serializers.ValidationError('Friend request has already been sent')
        
        return user_value