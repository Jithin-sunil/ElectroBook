from django.db import models

# Create your models here.
class tbl_admin(models.Model):
    admin_name=models.CharField(max_length=20)
    admin_contact=models.CharField(max_length=20)
    admin_email=models.CharField(max_length=20)
    admin_password=models.CharField(max_length=20)
    
class tbl_district(models.Model):
    district_name=models.CharField(max_length=20)


class tbl_category(models.Model):
    category_name=models.CharField(max_length=20)
    
class tbl_place(models.Model):
    place_name=models.CharField(max_length=30)
    place_pincode=models.CharField(max_length=30)
    district=models.ForeignKey(tbl_district,on_delete=models.CASCADE)

class tbl_local_place(models.Model):
    local_place_name=models.CharField(max_length=30)
    place=models.ForeignKey(tbl_place,on_delete=models.CASCADE)

class tbl_work_category(models.Model):
    work_category_name=models.CharField(max_length=40)

class tbl_subcategory(models.Model):
    subcategory_name=models.CharField(max_length=20)
    category=models.ForeignKey(tbl_category,on_delete=models.CASCADE)


