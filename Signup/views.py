import requests
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .models import AppUser
from .serializers import AppUserSerializer

class UserRegistration(APIView):
    permission_classes = (AllowAny,)

    def post(self, request, format=None):
        email = request.data['email']
        password = request.data['password']
        
        if not AppUser.objects.filter(email__exact=email).exists():
            serializer = AppUserSerializer(data=request.data)

            if serializer.is_valid(raise_exception=True):
                user = serializer.save()

                data = serializer.data

                token = self.auth({'email':email, 'password': password})

                userData = {}

                userData['firstname'] = user.firstname
                userData['lastname'] = user.lastname
                userData['email'] = user.email

                return Response({"Message": "User Created And Logged In Successfully", "Token": token, "User": userData, "Error": None}, status=status.HTTP_200_OK)
        return Response({"Message": "User Not Created Successfully", "Error": "User With Email Already Exists"}, status=status.HTTP_406_NOT_ACCEPTABLE)

    def auth(self, user):
        email = user.get('email', None)
        password = user.get('password', None)

        res = requests.post('http://127.0.0.1:8000/auth/login/', data={
            'email': email,
            'password': password
        })
        
        if res.status_code == 200:
            data = res.json()
            return data['Token']