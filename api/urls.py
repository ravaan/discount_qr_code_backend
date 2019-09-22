from django.conf.urls import url
from django.urls import include, path
from rest_framework import routers

from api.views import QRCodeView
from . import views

# router = routers.DefaultRouter()
# router.register(r'QRCode', views.QRCodeView,base_name='QRCode')

urlpatterns = [
    url(r'QRCode/', QRCodeView.as_view() )
]