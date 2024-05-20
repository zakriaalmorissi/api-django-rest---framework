from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, status, viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny, BasePermission, SAFE_METHODS
from django.conf import settings
from django.db import IntegrityError
from rest_framework.decorators import action
from django.http import Http404
from django.db.models import Q
from django.shortcuts import get_object_or_404

from .models import UserProfile, Follow, Post, Like, Comment, Image
from .serializers import ( 
                        ProfileSerializer, UserSerailize, 
                          PostSerialize, CommentSerialize,
                            LikeSerialize, ImageSerialize ,
                              ProfileDetialSerializer
                            )
from accounts.models import CustomUser





class RegisterUser(generics.CreateAPIView):
    permission_classes = [AllowAny]
    queryset = CustomUser.objects.all()
    serializer_class = UserSerailize

   



class UserProfileView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = UserProfile.objects.all()
    serializer_class = ProfileSerializer



class ProfilesViewActions(viewsets.ModelViewSet):
    """
    1. List all profiles
    2. Retrieve an individual profile
    3. Update an individual profile
    4. Handle the following actioons
    """
    permission_classes = [IsAuthenticated]
    queryset = UserProfile.objects.all()
    serializer_class = ProfileSerializer
    http_method_names = ['get', 'put', 'patch', 'delete']

    def create(self, reqest, *args, **kwargs):
              return Response({"data": "Creating profiles is not allowed"}, 
                              status=status.HTTP_405_METHOD_NOT_ALLOWED)


    def list(self, request, *args, **kwargs):
        profiles = self.get_queryset()
        serializer = ProfileDetialSerializer(profiles, many=True)
        return Response(serializer.data)
    
    def retrieve(self, request, *args, **kwargs):
        profile_id = kwargs.get('pk')
        try:
            instance = self.get_queryset().get(pk=profile_id)

        except UserProfile.DoesNotExist:
            return Response({"data":"not found"}, status=status.HTTP_404_NOT_FOUND)
        
        if request.user != instance.owner:
            # prevent the user from visting other users' profiles details 
            return Response({"data":"not Allowed"}, status=status.HTTP_403_FORBIDDEN)
         
        serialize = self.get_serializer(instance)
        return Response(serialize.data)

    def update(self, request, *args, **kwargs):
        user_profile = self.get_queryset()
        if request.user != user_profile.owner:
            # prevent the user from updating other users' profiles
            return Response({"data":"not allowed"},status=status.HTTP_403_FORBIDDEN)
            
        
        serialize = self.get_serializer(user_profile, data=request.data, partial=True)
        serialize.is_valid(raise_exception=True)
        serialize.save()

        return Response(serialize.data, status=status.HTTP_200_OK)   
        
    """
    To add custom actions to our viewsets we need to use the @action decorator
    This decorator allows to define additional methods that can be accessed through 
    specific endpoints and HTTP methods that can perform tasks not provided in the 
    standard ModelViewSet CRUD operations
    """
    
    @action(detail=True, methods=["PUT"])
    def follow(self, request, pk=None):
        follower =  UserProfile.objects.get(owner=request.user)
        followed = self.get_object()
        try:
            if request.user == followed.owner:
                return Response({"status":"you can't follow ur own profile"}, status=status.HTTP_401_UNAUTHORIZED)
            follower.follow(followed)

        except IntegrityError:
            return Response({'status':'already following'},status=status.HTTP_406_NOT_ACCEPTABLE)
        
        else:
            return Response({"status":"followed"})
        

    
    
class UserProfileFollowersActions(viewsets.ModelViewSet):

    """
    Query the profiles that follow and being followed by the current user's profile
    Handle the unfollowing, blocking and unblocking actions 
    """
    permission_classes = [IsAuthenticated]
    queryset = UserProfile.objects.all()
    serializer_class = ProfileDetialSerializer
    http_method_names = ['get','put','patch']


    
    @action(detail=True, methods=["GET"])
    def followers(self, request, pk=None):
        profile = self.get_object()
        followers = profile.followed_by.all()
        serialize = ProfileDetialSerializer(followers, many=True)

        return Response(serialize.data)
    
    @action(detail=True, methods=["GET"])
    def following(self, request, pk=None):
        profile = self.get_object()
        followers = profile.follows.all()
        serialize = ProfileDetialSerializer(followers, many=True)

        return Response(serialize.data)
    

    
        
    @action(detail=True, methods=["PUT"])
    def unfollow(self, request, pk=None):
        follower = UserProfile.objects.get(owner=request.user)
        followed = self.get_object()

        follower.unfollow(followed)
        return Response(status=status.HTTP_200_OK)
    

    @action(detail=True, methods=["POST"])
    def block(self, request, pk=None):
        pass
    

    @action(detail=True, methods=["POST"])
    def unblock(self, request, pk=None):
        pass
    
    

    

    
#-------------------------------------------------------------------------------------------------------
class AllPostsView(generics.ListAPIView):
    permission_classes = [AllowAny]
    queryset = Post.objects.all()
    serializer_class = PostSerialize


class PostsSerializeView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Post.objects.all()
    serializer_class = PostSerialize

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
    
    def get_queryset(self):
        return Post.objects.filter(author=self.request.user)
    
    def update(self, request, *args, **kwargs):
        post = self.get_object()
        if request.user != post.author:
            return Response({"status": "not allowed"}, status=status.HTTP_401_UNAUTHORIZED)
        
        serializer = self.get_serializer(post, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def destroy(self, request, *args, **kwargs):
        post = self.get_object()
        if request.user != post.author:
            return Response({"status": "not allowed"}, status=status.HTTP_401_UNAUTHORIZED)
        
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    @action(detail=True, methods=["post", "get"])
    def comment(self, request, pk=None):
        try:
            commented_post = self.get_queryset().get(pk=pk)
        except Post.DoesNotExist:
            return Response({"status": "not found"}, status=status.HTTP_404_NOT_FOUND)
        
        if request.method == "POST":
            comment_serializer = CommentSerialize(data=request.data)
            if comment_serializer.is_valid():
                comment_serializer.save(author=request.user, commented_on=commented_post)
                return Response(comment_serializer.data, status=status.HTTP_201_CREATED)
            return Response(comment_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        elif request.method == "GET":
            comments = Comment.objects.filter(commented_on=commented_post).order_by("-created_at")
            comment_serializer = CommentSerialize(comments, many=True)
            return Response(comment_serializer.data, status=status.HTTP_200_OK)
        
        return Response({"status": "method not allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    

    
    


    
    
    

    
    


      
    






























