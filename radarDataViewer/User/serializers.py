from rest_framework import serializers
from django.contrib.auth.models import User



class UserSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = User 
        fields = ['id', 'first_name','last_name','username', 'password', 'email', "is_staff", "is_superuser"]
        # fields = ['id', 'username', 'password', 'email']

class UpdateUserSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = User 
        fields = ['id', 'first_name','last_name','username', 'password', 'email', "is_staff", "is_superuser"]
#         {
#     "username": "adam",
#      "password": "Pass1234!",
#      "email": "adam@mail.com",
#      "first_name" : "adam",
#      "last_name" : "john"
# }
