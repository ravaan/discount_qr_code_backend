import uuid

from pyqrcode import create

from api.models import QRCode
from config import settings


def generate_qr_code(value: float, count: int) -> uuid:
    hash_code = uuid.uuid1().hex

    url = create(settings.WEB_URL + hash_code)

    filename = settings.IMAGES_PATH + "QRCode_" + str(value) + "_" + str(count) + ".png"
    url.png(filename, scale=25)

    return hash_code


def qr_code(value: float, count: int = 1):
    for index in range(count):
        hash_code = generate_qr_code(value, index + 1)
        QRCode.objects.create(
            qr_hash=hash_code,
            offer_value=value,
            expired=False
        )
