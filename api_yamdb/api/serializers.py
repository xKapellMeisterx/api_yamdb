from rest_framework import serializers

from .models import User



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('username', 'password')
        model = User
        
        
class EmailRegistration(serializers.Serializer):
    email = serializers.EmailField()
    username = serializers.CharField(max_length=50)
    
        

