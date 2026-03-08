from django.db import models
from Administrator.models import * 
from Guest.models import * 
 
class tbl_product(models.Model):
    product_name=models.CharField(max_length=30)
    product_photo=models.FileField(upload_to="Assets/Seller/product/")
    product_description=models.CharField(max_length=30)
    product_price=models.CharField(max_length=30)
    seller=models.ForeignKey(tbl_seller,on_delete=models.CASCADE)
    subcategory=models.ForeignKey(tbl_subcategory,on_delete=models.CASCADE)
   
class tbl_stock(models.Model):
    stock_count=models.CharField(max_length=30)
    product=models.ForeignKey(tbl_product,on_delete=models.CASCADE)
   