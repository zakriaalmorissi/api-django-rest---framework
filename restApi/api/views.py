from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, status, viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth.models import User
from django.db import IntegrityError
from rest_framework.decorators import action
from django.http import Http404
from django.shortcuts import get_object_or_404

from .models import UserProfile, Follow
from .serializers import ProfileSerializer, UserSerailize






class RegisterUser(generics.CreateAPIView):
    permission_classes = [AllowAny]
    queryset = User.objects.all()
    serializer_class = UserSerailize

   



class UserProfileView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = UserProfile.objects.all()
    serializer_class = ProfileSerializer



class ProfileDetialView(viewsets.ModelViewSet):
    """
    Retreive the user profile and update it 
    """
    permission_classes = [IsAuthenticated]
    queryset = UserProfile.objects.all()
    serializer_class = ProfileSerializer
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if request.user != instance.owner:
            # prevent the user from visting other users' profiles details 
            return Response({"data":"not Allowed"}, status=status.HTTP_403_FORBIDDEN)
        
        serialize = self.get_serializer(instance)
        return Response(serialize.data)

    def update(self, request, *args, **kwargs):
        user_profile = self.get_object()
        if request.user != user_profile.owner:
            # prevent the user from updating other users' profiles
            return Response({"data":"not allowed"},status=status.HTTP_403_FORBIDDEN)
        
        serialize = self.get_serializer(user_profile, data=request.data, partial=True)
        serialize.is_valid(raise_exception=True)
        serialize.save()

        return Response(serialize.data, status=status.HTTP_200_OK)
    
    def partial_update(self, request, *args, **kwargs):
       return self.update(request, *args, **kwargs)

    


class FollowProfilesView(viewsets.ModelViewSet):
    """
    Handle the following and unfollowing logics
    """
    permission_classes = [IsAuthenticated]
    queryset = UserProfile.objects.all()
    serializer_class = ProfileSerializer

    """
    To add custom actions to our viewsets we need to use the @action decorator
    This decorator allows to define additional methods that can be accessed through 
    specific endpoints and HTTP methods that can perform tasks not provided in the 
    standard ModelViewSet CRUD operations
    """
    @action(detail=True, methods=["POST"])
    def follow(self, request, pk=None):
        follower =  UserProfile.objects.get(owner=request.user)
        followed = self.get_object()
        try:
            if request.user == followed.owner:
                return Response({"status":"you can't follow ur own profile"}, status=status.HTTP_401_UNAUTHORIZED)
            follow = follower.follow(followed)

        except IntegrityError:
            return Response({'status':'already following'},status=status.HTTP_406_NOT_ACCEPTABLE)
        
        else:
            return Response({"status":"followed"})
        
        
    @action(detail=True, methods=["POST"])
    def unfollow(self, request, pk=None):
        follower = UserProfile.objects.get(owner=request.user)
        followed = self.get_object()

        follower.unfollow(followed)
        return Response(status=status.HTTP_200_OK)

      
    






























