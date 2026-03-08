from django.db import models
from Administrator.models import * 
# Create your models here.
class tbl_user(models.Model):
    user_name=models.CharField(max_length=30)
    user_email=models.CharField(max_length=30)
    user_contact=models.CharField(max_length=30)
    user_address=models.CharField(max_length=30)
    place=models.ForeignKey(tbl_place,on_delete=models.CASCADE)
    user_photo=models.FileField(upload_to="Assets/User/photo/")
    user_password=models.CharField(max_length=30)


class tbl_seller(models.Model):
    seller_name=models.CharField(max_length=30)
    seller_email=models.CharField(max_length=30)
    seller_contact=models.CharField(max_length=30)
    seller_address=models.CharField(max_length=30)
    place=models.ForeignKey(tbl_place,on_delete=models.CASCADE)
    seller_logo=models.FileField(upload_to="Assets/Seller/logo/")
    seller_proof=models.FileField(upload_to="Assets/Seller/proof/")
    seller_password=models.CharField(max_length=30)
    seller_status=models.IntegerField(default=0)


class tbl_electrician(models.Model):
    electrician_name=models.CharField(max_length=30)
    electrician_email=models.CharField(max_length=30)
    electrician_contact=models.CharField(max_length=30)
    electrician_address=models.CharField(max_length=30)
    local_place=models.ForeignKey(tbl_local_place,on_delete=models.CASCADE, null=True)
    work_category=models.ForeignKey(tbl_work_category,on_delete=models.CASCADE, null=True)
    electrician_photo=models.FileField(upload_to="Assets/Electrician/photo/")
    electrician_aadhar=models.FileField(upload_to="Assets/Electrician/aadhar/", null=True)
    electrician_pcc=models.FileField(upload_to="Assets/Electrician/pcc/", null=True)
    electrician_password=models.CharField(max_length=30)
    electrician_status=models.IntegerField(default=0)
