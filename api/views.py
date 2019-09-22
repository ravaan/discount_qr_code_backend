from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from api.serializers import QRCodePostSerializer, QRCodeGetSerializer
from api.utils.clean_up import clean_up
from api.utils.mailer import send_mail
from api.utils.qr import qr_code
from api.utils.zip_file import get_zip
from .models import QRCode


class QRCodeView(APIView):

    @staticmethod
    def post(request):
        serializer = QRCodePostSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        validated_data = serializer.validated_data
        offers = validated_data["offers"]

        for value, count in offers.items():
            qr_code(float(value), int(count))

        zip_name = get_zip()
        send_mail(zip_name)

        # delete all qr codes and zip files after sending the mail
        clean_up()

        return Response({"result": "QR Code generated and mailed"}, status=status.HTTP_200_OK)

    @staticmethod
    def get(request):
        serializer = QRCodeGetSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        validated_data = serializer.validated_data

        try:
            qr = QRCode.objects.get(qr_hash=validated_data["qr_hash"])
        except Exception as e:
            return Response(
                {
                    "result": "QR Code not found, try another hash",
                    "description": str(e)
                },
                status=status.HTTP_404_NOT_FOUND
            )

        if not qr.expired:
            qr.expired = True
            qr.save()
            return Response({"offer_value": qr.offer_value}, status=status.HTTP_200_OK)

        else:
            return Response({"result": "QR Code has already been used"}, status=status.HTTP_200_OK)
