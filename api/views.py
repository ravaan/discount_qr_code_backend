from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from api.serializers import QRCodePostSerializer, QRCodeGetSerializer
from api.utils.clean_up import clean_up
from api.utils.mailer import send_mail
from api.utils.zip_file import get_zip
from .models import QRCode
from api.utils.qr import generate_qr_code


class QRCodeView(APIView):

    def post(self, request):
        serializer = QRCodePostSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        validated_data = serializer.validated_data
        offers = validated_data["offers"]

        for value, count in offers.items():
            qr_directory = self.create_qr_code(float(value), int(count))

        zip_path, zip_name = self.zip_files()
        send_mail(zip_path, zip_name)
        clean_up([qr_directory, zip_path])

        return Response({"result": "QR Code generated and mailed"}, status=status.HTTP_200_OK)

    def get(self, request):
        serializer = QRCodeGetSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        validated_data = serializer.validated_data

        try:
            qr = QRCode.objects.get(qr_hash=validated_data["qr_hash"])
        except:
            return Response({"result": "QR Code not found, try another hash"}, status=status.HTTP_404_NOT_FOUND)

        if not qr.expired:
            qr.expired = True
            qr.save()
            return Response({"offer_value": qr.offer_value}, status=status.HTTP_200_OK)

        else:
            return Response({"result": "QR Code has already been used"}, status=status.HTTP_200_OK)

    def create_qr_code(self, value: float, count: int = 1) -> tuple:
        for index in range(count):
            hash_code, directory = generate_qr_code(value, index + 1)
            QRCode.objects.create(
                qr_hash=hash_code,
                offer_value=value,
                expired=False
            )
        return directory

    def zip_files(self):
        zip_name = "QRCode"
        zip_path, zip_name = get_zip(zip_name)

        return zip_path, zip_name

