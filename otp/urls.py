from django.urls import path, include
from rest_framework.routers import DefaultRouter
from otp import views

router = DefaultRouter()
app_name = 'otp'

urlpatterns = [
    path('', include(router.urls)),
    #---------------- send AnonymousMobile ----------------------#
    path('send-email/', views.SendOTPView.as_view(), name='send_code_email'),

]