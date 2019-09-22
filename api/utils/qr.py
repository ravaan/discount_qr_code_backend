import uuid
import os
from pyqrcode import QRCode, create


def generate_qr_code(value: float, count: int) -> uuid:
    s = "www.mysite.com/"
    hash_code = uuid.uuid1().hex

    url = create(s + hash_code)

    directory = "images/"

    filename = directory + "QRCode_" + str(value) + "_" + str(count) + ".png"
    url.png(filename, scale=25)

    return hash_code, directory

