import json
from datetime import timedelta
from django.utils import timezone
from random import randrange
from django.conf import settings
from django.shortcuts import render
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from otp.models import User
from otp.serializer import  SendOTPSerializer
from otp.tasks import send_verification_email


#from otp.tasks import send_verification_email


# class SendOTPView(APIView):
#     def post(self, request):
#         email = request.data.get('email', '')
#         if not email:
#             return Response({'error': 'Email is required'}, status=status.HTTP_400_BAD_REQUEST)
#
#         try:
#             user = User.objects.get(email=email)
#         except User.DoesNotExist:
#             return Response({'error': 'User with this email does not exist'}, status=status.HTTP_404_NOT_FOUND)
#
#         otp = generate_otp()
#         user.otp = otp
#         user.save()
#
#         # Send OTP email asynchronously with Celery
#         send_otp_email_task.delay(email, otp)
#         return Response({'message': 'OTP sent to your email'}, status=status.HTTP_200_OK)
# ---------------------------------------------------------------------------------------------------------------------
# send code to  email
# ---------------------------------------------------------------------------------------------------------------------
class SendOTPView(GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = SendOTPSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            user = User.objects.get(email=email)
            user.verify_email_code = str(randrange(100000, 999999))
            user.verify_email_code_expire_at = timezone.now() + timedelta(seconds=settings.EMAIL_VERIFY_EXPIRATION)
            user.save()
            data = {
                'email': email,
                'code': user.verify_email_code
            }
            send_verification_email.delay(json.dumps(data))
            return Response({'timeout': settings.EMAIL_VERIFY_EXPIRATION}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ---------------------------------------------------------------------------------------------------------------------
# Verify Mobile by email
# ---------------------------------------------------------------------------------------------------------------------
