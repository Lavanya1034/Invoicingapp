from rest_framework import serializers # type: ignore
from .models import UserModel,Item,Invoice
from django.contrib.auth import authenticate # type: ignore
from .models import UserManager
 

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField (write_only=True)

    class Meta:
        model = UserModel
        fields = ('username', 'password')

        def create(self, validated_data):
            user = UserModel.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data['email'],
            name=validated_data['name']
            )
            return user
        

class LoginSerializer (serializers.Serializer):
    username=serializers.CharField()
    password=serializers.CharField()
    def validate(self, data):

        user = authenticate(**data)
        print(user)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Incorrect creds")

        
class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model=Item
        exclude=["invoice"]
        
class InvoiceSerializer(serializers.ModelSerializer):
    items = ItemSerializer(many=True)  #connecting both serializers
    class Meta:
        model=Invoice
        fields="__all__"
  