from django.db import models
from django.conf import settings

# Create your models here.

class BaseModel(models.Model):
    is_deleted = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='%(class)s_createdby', null=True, on_delete=models.PROTECT)
    modified_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='%(class)s_modifiedby', null=True, blank=True, on_delete=models.PROTECT)

    class Meta:
       abstract = True

    def delete(self):
        self.is_deleted = True
        self.is_active = False
        self.save()

class Country(BaseModel):
    name = models.CharField(max_length=100)
    symbol = models.CharField(max_length=10)
    description = models.TextField(blank=True, null=True)

    class Meta:
        db_table = "tbl_country_mst"

class BillingMst(BaseModel):
    invoice_number = models.CharField(max_length=50)
    bill_to =  models.CharField(max_length=100)
    bill_to_email =  models.CharField(max_length=100)
    bill_to_address =  models.TextField(blank=True, null=True)
    bill_from = models.CharField(max_length=100)
    bill_from_address = models.CharField(max_length=100)
    bill_from_email =  models.TextField(blank=True, null=True)
    notes =  models.TextField(blank=True, null=True)
    sub_total = models.CharField(max_length=20)
    total = models.CharField(max_length=20)
    tax_rate = models.CharField(max_length=20,blank=True, null=True)
    tax_amount = models.CharField(max_length=20,blank=True, null=True)
    discount_amount = models.CharField(max_length=20,blank=True, null=True)
    discount_rate = models.CharField(max_length=20,blank=True, null=True)
    currency = models.CharField(max_length=20,blank=True, null=True)

    class Meta:
        db_table = "tbl_billing_mst"

class BillingDetail(BaseModel):
    mst_ref_id = models.ForeignKey(BillingMst, on_delete=models.PROTECT,related_name='items')
    name = models.CharField(max_length=255)
    price = models.CharField(max_length=20)
    quantity = models.CharField(max_length=10)
    description = models.TextField(blank=True, null=True)

    class Meta:
        db_table = "tbl_billing_detail"