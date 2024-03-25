from rest_framework import serializers
from .models import Message,CustomUser

class MessageSerializer(serializers.ModelSerializer):
    sender = serializers.SlugRelatedField(slug_field='username', read_only=True)
    sender_profile_picture = serializers.SerializerMethodField()
    # receiver_profile_picture = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = ['id', 'sender', 'receiver', 'content', 'timestamp','sender_profile_picture']
        
    def get_sender_profile_picture(self, obj):
        # Access sender's profile picture URL from the message sender (assuming sender is a CustomUser instance)
        return obj.sender.profile_picture.url if obj.sender.profile_picture else None

    # def get_receiver_profile_picture(self, obj):
    #     # Access receiver's profile picture URL from the message receiver (assuming receiver is a CustomUser instance)
    #     return obj.receiver.profile_picture.url if obj.receiver.profile_picture else None
    
class CustomUserSerializer(serializers.ModelSerializer):
    profile_picture = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'profile_picture']

    def get_profile_picture(self, obj):
        # Assuming profile_picture field contains the URL to the user's profile picture
        if obj.profile_picture:
            return obj.profile_picture.url
        return None