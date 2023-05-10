from django.shortcuts import render
from django.db import transaction
from .serializers import User, BaseUserSerializer, FriendRequestSerializer, UserSerializer
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView
from rest_framework.viewsets import ReadOnlyModelViewSet, GenericViewSet
from rest_framework import mixins
from rest_framework.exceptions import NotFound

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

class UserViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin, GenericViewSet):
    lookup_field = 'username'

    def get_queryset(self):
        if self.action == 'create':
            return User.objects.all()
        return User.objects.exclude(id=self.request.user.id)

    def get_serializer_class(self):
        if self.request.user.is_anonymous:
            return BaseUserSerializer
        return UserSerializer


class FriendViewSet(mixins.ListModelMixin, mixins.DestroyModelMixin, GenericViewSet):
    serializer_class = UserSerializer
    lookup_field = 'username'
    
    def get_queryset(self):
        return self.request.user.friends.all()
    
    def perform_destroy(self, instance):
        self.request.user.friends.remove(instance)
    

class FriendRequestViewSet(mixins.ListModelMixin, mixins.CreateModelMixin, mixins.DestroyModelMixin, GenericViewSet):
    lookup_field = 'username'

    def get_queryset(self):
        if self.action == 'destroy':
            return User.objects.all()

        friend_request_type = self.request.query_params.get('type')
        incoming_friend_requests = self.request.user.incoming_friend_requests.all()
        outgoing_friend_requests = self.request.user.outgoing_friend_requests.all()

        if friend_request_type == 'incoming':
            return incoming_friend_requests
        elif friend_request_type == 'outgoing':
            return outgoing_friend_requests

        return incoming_friend_requests.union(outgoing_friend_requests)
    
    def get_serializer_class(self):
        if self.action == 'create':
            return FriendRequestSerializer
        return UserSerializer

    def perform_create(self, serializer):
        new_friend_request = serializer.validated_data['to_user']
        if self.request.user.incoming_friend_requests.filter(id=new_friend_request.id).exists():
            with transaction.atomic():
                self.request.user.friends.add(new_friend_request)
                new_friend_request.outgoing_friend_requests.remove(self.request.user)
        else:
            self.request.user.outgoing_friend_requests.add(new_friend_request)

    def perform_destroy(self, instance):
        self.request.user.incoming_friend_requests.remove(instance)  
# Create your views here.