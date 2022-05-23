from django.db import models


# Create your models here.
class VmItem(models.Model):
    item_name = models.CharField(verbose_name='Name', max_length=255)
    item_price = models.DecimalField(max_digits=6, decimal_places=2)
    item_inv = models.IntegerField(blank=True, null=True)
    item_img = models.ImageField(verbose_name='Image', upload_to='Itemimages/', blank=True, null=True)

    class Meta:
        verbose_name_plural = 'Item'
        verbose_name = "Item"

    def __str__(self):
        return self.item_name



class Transaction(models.Model):
    made_by = models.CharField(max_length=255, null=True, blank=True)
    made_on = models.DateTimeField(auto_now_add=True)
    amount = models.IntegerField()
    item_id = models.IntegerField(null=True, blank=True)
    order_id = models.CharField(unique=True, max_length=100, null=True, blank=True)
    checksum = models.CharField(max_length=100, null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.order_id is None and self.made_on and self.id:
            self.order_id = self.made_on.strftime('PAY2ME%Y%m%dODR') + str(self.id)
        return super().save(*args, **kwargs)


