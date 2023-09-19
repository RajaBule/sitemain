from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

User = get_user_model()

class EmailBackend(ModelBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        try:
            # Try to find the user by email
            user = User.objects.get(email=email)

            # Check if the password is valid for the user
            if user.check_password(password):
                return user
            else:
                print('Invalid Password')
        except User.DoesNotExist:
            pass

        try:
            # Try to find the user by username
            user = User.objects.get(email=email)

            # Check if the password is valid for the user
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            print('User Login Error: The user email ' + email + 'was not found')
            pass

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None, print('No user with that email')