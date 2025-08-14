from rest_framework import serializers
from .models import AppUser, Student, Lecturer

class AppUserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True)
    firstname = serializers.CharField(required=True)
    lastname = serializers.CharField(required=True)
    matric_no = serializers.CharField(required=False)
    lec_id = serializers.CharField(required=False)

    class Meta:
        model = AppUser
        fields = "__all__"


    def create(self, data):
        matric = data.pop('matric_no', None)
        lec = data.pop('lec_id', None)
        user = AppUser.objects.create_user(**data)

        if user:
            if matric:
                student = Student.objects.create(user=user, matric_no=matric)
            elif lec:
                lecturer = Lecturer.objects.create(user=user, lec_id=lec)
            return user
        return None
