from rest_framework import serializers
from .models import UserProfile, Follow
from django.contrib.auth.models import User


class UserSerailize(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username','email','password']

    
    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email= validated_data['email'],
            password=validated_data['password']
        )
        UserProfile.objects.create(owner=user)
        return user
       

class ProfileDetialSerializer(serializers.ModelSerializer):
    profile_owner = serializers.SerializerMethodField()
    class Meta:
        model = UserProfile
        fields = ['id','profile_owner','image']

    def get_profile_owner(self, obj):
        return obj.owner.first_name if obj.owner.first_name else obj.owner.username
        

class ProfileSerializer(serializers.ModelSerializer):

    profile_owner = serializers.SerializerMethodField()
    followers = serializers.SerializerMethodField()
    following = serializers.SerializerMethodField()
    is_following = serializers.SerializerMethodField()
    is_followed = serializers.SerializerMethodField()

    class Meta:
        model = UserProfile
        fields = [

            'id','profile_owner','image', 'first_name','last_name','follows',
            'followers','following', 'is_following',
            'is_followed','created_at', 'updated_at'

            ]
        
    def get_profile_owner(self, obj):
        return obj.owner.first_name if obj.owner.first_name else obj.owner.username
        

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
        return obj.follows.filter(id=user.my_profile.id).exists()
      
    
    def get_is_followed(self, obj):
        request = self.context.get('request', None)
        if request is None:
            return True
        
        user = request.user
        return obj.followed_by.filter(id=user.my_profile.id).exists()



class FollowSerializer(serializers.ModelSerializer):
    pass