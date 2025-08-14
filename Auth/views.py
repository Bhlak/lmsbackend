from django.contrib.auth import logout
from django.shortcuts import get_object_or_404

from rest_framework import status 
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.authentication import SessionAuthentication, TokenAuthentication

from Signup.models import AppUser
from Signup.serializers import AppUserSerializer
from .serializers import LoginSerializer


@api_view(['GET'])
def getUsers(request):
    users = AppUser.objects.all()
    serializer = AppUserSerializer(users, many=True)
    return Response(serializer.data)


class LoginView(APIView):
    permission_classes = ( AllowAny, )



    def post(self, request, format=None):

        if request.user.is_authenticated:
            return Response({"Message": "User Already Logged In", "Error": None}, status=status.HTTP_200_OK)
        
        data = request.data

        serializer = LoginSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        is_staff = serializer.validated_data["staff"]


        if not user.check_password(data['password']):
            return Response({"Message": "User Authentication Failed", "Error": "Incorrect Details"}, status=status.HTTP_404_NOT_FOUND)

        token, created = Token.objects.get_or_create(user=user)

        userSerializer = AppUserSerializer(user)
        filteredUser = {key: userSerializer.data[key] for key in ['email', 'firstname', 'lastname']}
        filteredUser["is_staff"] = is_staff
        # print(filteredUser)
        return Response({"Message": "User Logged In Successfully","Token": token.key, "User": filteredUser, "Error": None}, status=status.HTTP_200_OK)


class LogoutView(APIView):
    permission_classes = ( IsAuthenticated, )
    authentication_classes = ( TokenAuthentication, )

    def get(self, request, format=None):
        if request.user.auth_token:
            request.user.auth_token.delete()
            logout(request)
            return Response({"Message": "User Logged Out Successfully", "Error": None}, status=status.HTTP_200_OK)
        return Response({"Message": None, "Error": "User Does Not Have An Auth Token"}, status=status.HTTP_401_UNAUTHORIZED)


class GetUserDetails(APIView):
    permission_classes = ( IsAuthenticated, )
    authentication_classes = ( TokenAuthentication, )

    def get(self, request, format=None):
        user = AppUser.objects.get(email__exact=request.user.email)

        data = dict()

        data['email'] = user.email
        data['firstname'] = user.firstname
        data['lastname'] = user.lastname
        return Response({"Message": "User Fetched Successfully","Data": data, "Error": None}, status=status.HTTP_200_OK)

class Test(APIView):
    permission_classes = ( IsAuthenticated, )
    authentication_classes = ( TokenAuthentication, )
    def get(self, request):
        return Response({"Message": f"Test passed for user {request.user.email}"}, status=status.HTTP_200_OK)