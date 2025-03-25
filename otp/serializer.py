from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from otp.models import User
from django.contrib.auth import get_user_model
User = get_user_model()

# ---------------------------------------------------------------------------------------------------------------------
# validation code
# ---------------------------------------------------------------------------------------------------------------------

# ---------------------------------------------------------------------------------------------------------------------
# send email code
# ---------------------------------------------------------------------------------------------------------------------

class SendOTPSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = ('email',)

    def validate_email(self, value):
        user = User.objects.filter(email=value).first()
        if user is None:
            raise serializers.ValidationError({"email": 'email was not registered'})
        return value
