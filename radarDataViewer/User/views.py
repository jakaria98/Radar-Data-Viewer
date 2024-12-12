from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, throttle_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, login
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
from django.contrib.auth.models import User
from .serializers import UserSerializer

class LoginAnonThrottle(AnonRateThrottle):
    rate = '5/min'  # Limit unauthenticated users to 5 requests per minute

class LoginUserThrottle(UserRateThrottle):
    rate = '10/min'  # Limit authenticated users to 10 requests per minute

@api_view(['POST'])
@throttle_classes([LoginAnonThrottle, LoginUserThrottle])
def login_view(request):
    # Validate input fields
    username = request.data.get('username')
    password = request.data.get('password')

    if not username or not password:
        return Response(
            {"detail": "Username and password are required"},
            status=status.HTTP_400_BAD_REQUEST
        )

    # Authenticate user
    user = authenticate(request, username=username, password=password)
    if user is None:
        return Response(
            {"detail": "Invalid credentials"},
            status=status.HTTP_400_BAD_REQUEST
        )

    # Use session-based login
    login(request, user)

    # Serialize user data
    serializer = UserSerializer(user)
    return Response(
        {
            'message': "Login successful",
            'user': serializer.data,
        },
        status=status.HTTP_200_OK
    )


@api_view(['POST'])
def register(request):
    # Validate input fields
    required_fields = ['username', 'password', 'email']
    for field in required_fields:
        if field not in request.data:
            return Response(
                {"detail": f"{field} is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )
    
    # Serialize the user data
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        user.set_password(request.data['password'])  # Hash the password
        user.save()
        
        # Generate a token for the user
        token, created = Token.objects.get_or_create(user=user)
        return Response(
            {
                'token': token.key,
                'user': serializer.data,
                'message': "User created successfully",
            },
            status=status.HTTP_201_CREATED,
        )
    
    # Return validation errors
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

########################## Not working
########################## Not working
########################## Not working
@api_view(['PUT'])
def update_user(request):
    user = request.user
    serializer = UpdateUserSerializer(user, data=request.data)
    if serializer.is_valid():
        serializer.save()
        # user = User.objects.get(username=request.data['username'])
        # user.set_password(request.data['password'])
        # user.save()
        # token = Token.objects.create(user=user)
        return Response({'user': serializer.data, "message" : "Updated User info Succesfully"})
    return Response(serializer.errors, status=status.HTTP_200_OK)
########################## Not working
########################## Not working
########################## Not working
"""
@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def test_token(request):
    return Response("passed for {}".format(request.user.email))
"""
