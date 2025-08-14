from Signup.models import AppUser
from rest_framework import serializers

from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate

class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    password  = serializers.CharField(write_only=True)

    class Meta:
        model = AppUser
        fields = ["email", "password", "is_staff"]

    def validate(self, data):
        email = data.get('email', None)
        password = data.get("password", None)

        emu = get_object_or_404(AppUser, email=email)
        if emu.check_password(password):
                user = authenticate(email=email, password=password)
                if user:
                    data["user"] = user
                    data["staff"] = user.is_staff
                else:
                    raise ValueError("Authentication Error")
        else:
            raise ValueError("Incorrect Password")
        return data