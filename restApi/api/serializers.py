from rest_framework import serializers
from .models import UserProfile, Post, Image,Comment, Like
from accounts.models import CustomUser


class UserSerailize(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id','first_name','email','password']

    
    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            email= validated_data['email'],
            password=validated_data['password']
        )
        UserProfile.objects.create(owner=user,first_name=validated_data['first_name'])
        return user
       

class ProfileDetialSerializer(serializers.ModelSerializer):
    owner = serializers.StringRelatedField()
    class Meta:
        model = UserProfile
        fields = ['id','first_name','last_name','owner','image']


class ProfileSerializer(serializers.ModelSerializer):

    owner = serializers.StringRelatedField()
    followers = serializers.SerializerMethodField()
    following = serializers.SerializerMethodField()
    is_following = serializers.SerializerMethodField()
    is_followed = serializers.SerializerMethodField()

    class Meta:
        model = UserProfile
        fields = [

            'id','owner','image', 'first_name','last_name',
            'followers','following', 'is_following',
            'is_followed','created_at', 'updated_at'

            ]
        

    def get_followers(self, obj):
        followers = obj.followed_by.all()

        return ProfileDetialSerializer(followers, many=True, context=self.context).data
    

    def get_following(self, obj):
        following = obj.follows.all()

        return ProfileDetialSerializer(following, many=True, context=self.context).data
    
    def get_is_following(self, obj):
        request = self.context.get('request', None)
        if request is None:
            return False
        
        user = request.user
        return obj.follows.filter(id=user.profile.id).exists()
      
    
    def get_is_followed(self, obj):
        request = self.context.get('request', None)
        if request is None:
            return True
        
        user = request.user
        return obj.followed_by.filter(id=user.profile.id).exists()
    



#--------------------------------------------------------------------------------------------------------------------------------
# serialize the post model and its related models

class CommentSerialize(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()
    class Meta:
        model = Comment
        fields = ['id','author','content','created_at']

    def get_author(self, obj):
        return obj.author.first_name if obj.author.first_name else obj.author.email
    



class LikeSerialize(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()
    class Meta:
        model = Like
        fields = ['id','author','liked_post','done_at']
    
    def get_author(self, obj):
        return obj.author.first_name if obj.author.first_name else obj.author.email
    

class ImageSerialize(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['id', 'image']



class PostSerialize(serializers.ModelSerializer):
    author = serializers.StringRelatedField()
    comments = CommentSerialize(many=True, read_only=True)
    likes = LikeSerialize(many=True, read_only=True)
    images = ImageSerialize(many=True, required=False)

    class Meta:
        model = Post
        fields = [
            'id', 'author','content',
            'video','images','created_at', 
            'update_at', 'comments','likes'
        ]





    














