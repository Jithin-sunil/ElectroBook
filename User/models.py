from django.db import models
from Guest.models import * 
from Seller.models import *
# Create your models here.
class tbl_complaint(models.Model):
    complaint_title=models.CharField(max_length=30)
    complaint_content=models.CharField(max_length=30)
    complaint_date=models.DateField(auto_now_add=True)
    complaint_status=models.IntegerField(default=0)
    complaint_reply=models.CharField(max_length=30)
    complaint_replydate=models.DateField(null=True)
    user=models.ForeignKey(tbl_user,on_delete=models.CASCADE)
    product=models.ForeignKey(tbl_product,on_delete=models.CASCADE)

    


class tbl_booking(models.Model):
    booking_date = models.DateField(auto_now_add=True)
    booking_amount = models.CharField(max_length=30)
    booking_status = models.IntegerField(default=0)
    user = models.ForeignKey(tbl_user, on_delete=models.CASCADE, null=True)
    electrician = models.ForeignKey(tbl_electrician, on_delete=models.CASCADE, null=True)

class tbl_work_booking(models.Model):
    user = models.ForeignKey(tbl_user, on_delete=models.CASCADE)
    electrician = models.ForeignKey(tbl_electrician, on_delete=models.CASCADE)
    booking_date = models.DateField(auto_now_add=True)
    work_date = models.DateField()
    work_details = models.TextField()
    booking_status = models.IntegerField(default=0)
    estimate_details = models.TextField(null=True)
    estimate_amount = models.CharField(max_length=30, null=True)
   

class tbl_cart(models.Model):
    cart_qty = models.IntegerField(default=1)
    cart_status = models.IntegerField(default=0)
    product = models.ForeignKey(tbl_product, on_delete=models.CASCADE)
    booking = models.ForeignKey(tbl_booking, on_delete=models.CASCADE)
    electrician = models.ForeignKey(tbl_electrician, on_delete=models.CASCADE,null=True)


class tbl_feedback(models.Model):
    feedback_name=models.CharField(max_length=30)
    user=models.ForeignKey(tbl_user,on_delete=models.CASCADE,null=True)
    seller=models.ForeignKey(tbl_seller,on_delete=models.CASCADE,null=True)



class tbl_rating(models.Model):
    rating_data=models.IntegerField()
    user_review=models.CharField(max_length=500)
    product=models.ForeignKey(tbl_product,on_delete=models.CASCADE)
    user=models.ForeignKey(tbl_user,on_delete=models.CASCADE)
    datetime=models.DateTimeField(auto_now_add=True)


class tbl_electrician_rating(models.Model):
    rating_data = models.IntegerField()
    user_review = models.CharField(max_length=500)
    electrician = models.ForeignKey(tbl_electrician, on_delete=models.CASCADE)
    user = models.ForeignKey(tbl_user, on_delete=models.CASCADE)
    datetime = models.DateTimeField(auto_now_add=True)


class tbl_electrician_gallery(models.Model):
    gallery_photo = models.FileField(upload_to="Assets/Electrician/gallery/")
    caption = models.CharField(max_length=200, null=True, blank=True)
    electrician = models.ForeignKey(tbl_electrician, on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now_add=True)




  
