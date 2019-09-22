from django.db import models


class QRCode(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    qr_hash = models.CharField(blank=False, max_length=36)
    offer_value = models.FloatField(blank=False)
    expired = models.BooleanField(default=False, blank=False)

    def __str__(self):
        return '%s %s %s' % (self.offer_value, self.qr_hash, self.expired)