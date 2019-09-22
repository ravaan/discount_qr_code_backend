from django.conf.urls import url

from api.views import QRCodeView

urlpatterns = [
    url(r'QRCode/', QRCodeView.as_view())
]
