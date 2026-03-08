from django.shortcuts import render, redirect
from Guest.models import *
from Administrator.models import *
from Seller.models import *
from User.models import *
from datetime import date
from django.db.models import Sum
from django.http import JsonResponse
from django.db.models import Sum, Count
from django.db.models.functions import TruncMonth
from django.utils import timezone
from datetime import datetime

# Create your views here.

def logout(request):
    del request.session['sid']
    return redirect('Guest:login')
    
def myprofile(request):
    seller=tbl_seller.objects.get(id=request.session["sid"])
    return render(request,'Seller/MyProfile.html',{'seller':seller})

def editprofile(request):
    seller=tbl_seller.objects.get(id=request.session["sid"])
    if request.method=="POST":
        seller.seller_name=request.POST.get('txt_name')
        seller.seller_email=request.POST.get('txt_email')
        seller.seller_contact=request.POST.get('txt_contact')
        seller.seller_address=request.POST.get('txt_address')
        seller.save()
        return redirect('Seller:myprofile')
    else:
        return render(request,'Seller/EditProfile.html',{'seller':seller})

def changepassword(request):
    seller=tbl_seller.objects.get(id=request.session["sid"])
    dbpass=seller.seller_password
    if request.method=="POST":
        oldpassword=request.POST.get('txt_oldpass')
        newpassword=request.POST.get('txt_newpass')
        confirmpassword=request.POST.get('txt_conpass')
        if oldpassword==dbpass and newpassword==confirmpassword:
            seller.seller_password=newpassword
            seller.save()
            return redirect("Seller:myprofile")
    return render(request,'Seller/ChangePassword.html',{'seller':seller})

def sellerhomepage(request):
    if 'sid' not in request.session:
        return redirect('Guest:login')
    seller_id = request.session['sid']
    products = tbl_product.objects.filter(seller=seller_id)[:8]
    product_count = tbl_product.objects.filter(seller=seller_id).count()
    order_count = tbl_cart.objects.filter(product__seller=seller_id, cart_status__gte=2).values('booking').distinct().count()
    return render(request, 'Seller/Sellerhomepage.html', {'products': products, 'product_count': product_count, 'order_count': order_count})

def product(request):
    sellerid=tbl_seller.objects.get(id=request.session["sid"])
    category=tbl_category.objects.all()
    subcategory=tbl_subcategory.objects.all()
    product=tbl_product.objects.filter(seller=sellerid)
    for i in product:
        total_stock = tbl_stock.objects.filter(product=i.id).aggregate(total=Sum('stock_count'))['total']
        total_cart = tbl_cart.objects.filter(product=i.id, cart_status__gt=1).aggregate(total=Sum('cart_qty'))['total']
        # print(total_stock)
        # print(total_cart)
        if total_stock is None:
            total_stock = 0
        if total_cart is None:
            total_cart = 0
        total =  total_stock - total_cart
        i.total_stock = total
    if request.method=='POST':
        product_name=request.POST.get("txt_name")
        product_description=request.POST.get("txt_desc")
        product_photo=request.FILES.get('txt_photo')
        product_price=request.POST.get("txt_price")
        subcategory_id=tbl_subcategory.objects.get(id=request.POST.get("subcategory"))
        seller_id=tbl_seller.objects.get(id=request.session["sid"])
        tbl_product.objects.create(product_name=product_name,product_description=product_description,product_photo=product_photo,product_price=product_price,subcategory=subcategory_id,seller=seller_id,)
        return redirect('Seller:product')
    else:
        return render(request,'Seller/Product.html',{'category':category,'subcategory':subcategory,'product':product})

def deleteproduct(request,did):
    tbl_product.objects.get(id=did).delete()
    return redirect('Seller:product')


def ajaxsubcategory(request):
    subcategory=tbl_subcategory.objects.filter(category=request.GET.get('did'))
    return render(request,'Seller/ajaxsubcategory.html',{'subcategory':subcategory})

def addstock(request,id):
    stock=tbl_stock.objects.filter(product=id)
    if request.method=='POST':
        tbl_stock.objects.create(stock_count=request.POST.get("txt_count"),product=tbl_product.objects.get(id=id),)
        return redirect('Seller:addstock',id=id)
    else:
        return render(request,'Seller/Addstock.html',{'stock':stock})



    
def feedback(request):
    sellerid=tbl_seller.objects.get(id=request.session["sid"])
    feedback=tbl_feedback.objects.filter(seller=sellerid)
    if request.method=='POST':
        feedback_name=request.POST.get("txt_content")
        tbl_feedback.objects.create(feedback_name=feedback_name,seller=sellerid,)
        return redirect('Seller:feedback')
    else:
        return render(request,'Seller/Feedback.html',{'feedback':feedback})



def viewcomplaint(request):
    complaint=tbl_complaint.objects.filter(complaint_status=0,product__seller=request.session["sid"])
    Solvedcomplaint=tbl_complaint.objects.filter(complaint_status=1,product__seller=request.session["sid"])
    if request.method=="POST":
        return redirect('Seller:viewcomplaint')
    else:
         return render(request,'Seller/Viewusercomplaint.html',{'complaint':complaint,'Solvedcomplaint':Solvedcomplaint})


def replynow(request,cid):
    complaint=tbl_complaint.objects.get(id=cid)
    if request.method=="POST":
        complaint.complaint_reply=request.POST.get('reply')
        complaint.complaint_replydate=date.today()
        complaint.complaint_status=1
        complaint.save()
        return redirect('Seller:viewcomplaint')
    else:
        return render(request,'Seller/Replynow.html',{'complaint':complaint})


from collections import defaultdict

def viewbooking(request): 
    seller_id = request.session["sid"]
    cart_items = tbl_cart.objects.filter(
        product__seller=seller_id,
        cart_status__gte=2
    ).select_related('booking', 'product', 'booking__user', 'booking__electrician')

    grouped_cart = defaultdict(list)
    for item in cart_items:
        grouped_cart[item.booking.id].append(item)

    return render(request, 'Seller/viewbooking.html', {'cart': dict(grouped_cart)})


def packorder(request, id):
    cart_item = tbl_cart.objects.get(id=id)
    cart_item.cart_status = 3
    cart_item.save()
    return redirect('Seller:viewbooking')

def shiporder(request, id):
    cart_item = tbl_cart.objects.get(id=id)
    cart_item.cart_status = 4
    cart_item.save()
    return redirect('Seller:viewbooking')

def outfordelivery(request, id):
    cart_item = tbl_cart.objects.get(id=id)
    cart_item.cart_status = 5
    cart_item.save()
    return redirect('Seller:viewbooking')

def delivered(request, id):
    cart_item = tbl_cart.objects.get(id=id)
    cart_item.cart_status = 6
    cart_item.save()
    return redirect('Seller:viewbooking')



def viewelectrician(request,did):
    delivery=tbl_electrician.objects.get(id=did)
    return render(request,'Seller/viewelectrician.html',{'delivery':delivery})

def viewreport(request):
    return render(request,"Seller/ViewReport.html")

def pdtchart(request):
    try:
        seller_id = request.session.get("sid")

        sales_data = tbl_cart.objects.filter(product__seller=seller_id) \
            .values('product') \
            .annotate(sales_count=Count('product')) \
            .order_by('-sales_count')

        pie_data = {
            'labels': [tbl_product.objects.get(id=data['product']).product_name for data in sales_data],
            'data': [data['sales_count'] for data in sales_data]
        }

        products = tbl_product.objects.filter(seller=seller_id)

        # Monthly total sales data
        monthly_sales_data = tbl_cart.objects.filter(product__in=products) \
            .annotate(month=TruncMonth('booking__booking_date')) \
            .values('month') \
            .annotate(total_sales=Sum('booking__booking_amount')) \
            .order_by('month')

        all_months_names = [
            'January', 'February', 'March', 'April', 'May', 'June',
            'July', 'August', 'September', 'October', 'November', 'December'
        ]
        month_sales_map = {i: 0 for i in range(1, 13)} 

        for entry in monthly_sales_data:
            month_number = entry['month'].month
            month_sales_map[month_number] = entry['total_sales']
        bar_labels = all_months_names
        bar_data = [month_sales_map[i] for i in range(1, 13)]

        return JsonResponse({
            'pie': pie_data,
            'bar': {
                'labels': bar_labels,
                'datasets': [{
                    'label': 'Total Sales',
                    'data': bar_data,
                    'backgroundColor': 'rgba(0, 123, 255, 0.5)',
                    'borderColor': 'rgba(0, 123, 255, 1)',
                    'borderWidth': 1
                }]
            }
        })

    except tbl_seller.DoesNotExist:
        return JsonResponse({'error': 'Seller not found'}, status=404)




