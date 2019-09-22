from rest_framework import serializers
from .models import  QRCode


class QRCodePostSerializer(serializers.Serializer):
    offers = serializers.DictField()


class QRCodeGetSerializer(serializers.Serializer):
    qr_hash = serializers.CharField(max_length=36)