from rest_framework import serializers
from .models import AppUser

class AppUserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    firstname = serializers.CharField(required=True)
    lastname = serializers.CharField(required=True)
    matric_no = serializers.CharField(write_only=True, required=False)
    lec_id = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = AppUser
        fields = "__all__"


    def create(self, data):
        user = AppUser.objects.create_user(**data)

        if user:
            return user
        return None
