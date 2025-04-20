from django.contrib.auth.base_user import BaseUserManager

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, **extras):
        if not email:
            raise ValueError("Email required")
        if not password:
            raise ValueError("Password required")
        try:
            email = self.normalize_email(email)
            user = self.model(email=email, **extras)
            user.set_password(password)
            user.save()
            return user
        except Exception as e:
            print(f"Exception E: {e}")
    
    def create_superuser(self, email, password, *args, **kwargs):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password
            )
        
        user.is_staff = True
        user.is_superuser = True

        if not user.is_staff:
            raise ValueError("Superuser must be staff")
        elif not user.is_superuser:
            raise ValueError("Superuser must BE a superuser")
        
        user.save()
        return user