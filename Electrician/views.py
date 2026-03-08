from django.shortcuts import render, redirect
from Guest.models import *
from Administrator.models import *
from User.models import *
from Seller.models import *
from django.db.models import Sum, Count, Avg

def logout(request):
    del request.session['did']
    return redirect('Guest:login')

def myprofile(request):
    electrician = tbl_electrician.objects.get(id=request.session["did"])
    gallery = tbl_electrician_gallery.objects.filter(electrician=electrician).order_by('-uploaded_at')[:12]
    ratings = tbl_electrician_rating.objects.filter(electrician=electrician).order_by('-datetime')[:5]
    avg_rating = tbl_electrician_rating.objects.filter(electrician=electrician).aggregate(avg=Avg('rating_data'))['avg']
    rating_count = tbl_electrician_rating.objects.filter(electrician=electrician).count()
    return render(request, 'Electrician/MyProfile.html', {
        'electrician': electrician,
        'gallery': gallery,
        'ratings': ratings,
        'avg_rating': round(avg_rating or 0, 1),
        'rating_count': rating_count
    })

def editprofile(request):
    electrician=tbl_electrician.objects.get(id=request.session["did"])
    if request.method=="POST":
        electrician.electrician_name=request.POST.get('txt_name')
        electrician.electrician_email=request.POST.get('txt_email')
        electrician.electrician_contact=request.POST.get('txt_contact')
        electrician.electrician_address=request.POST.get('txt_address')
        if 'electrician_photo' in request.FILES:
            electrician.electrician_photo=request.FILES['electrician_photo']
        electrician.save()
        return redirect('Electrician:myprofile')
    else:
        return render(request,'Electrician/EditProfile.html',{'electrician':electrician})

def changepassword(request):
    electrician=tbl_electrician.objects.get(id=request.session["did"])
    dbpass=electrician.electrician_password
    if request.method=="POST":
        oldpassword=request.POST.get('txt_oldpass')
        newpassword=request.POST.get('txt_newpass')
        confirmpassword=request.POST.get('txt_conpass')
        if oldpassword==dbpass:
            if newpassword==confirmpassword:
                electrician.electrician_password=newpassword
                electrician.save()
                return redirect("Electrician:myprofile")
    else:
        return render(request,'Electrician/ChangePassword.html',{'electrician':electrician})

def dahomepage(request):
    if 'did' not in request.session:
        return redirect('Guest:login')
    return render(request,'Electrician/homepage.html')

def my_bookings(request):
    bookings = tbl_work_booking.objects.filter(electrician=request.session["did"]).order_by('-booking_date')
    return render(request, 'Electrician/my_bookings.html', {'bookings': bookings})

def accept_booking(request, id):
    booking = tbl_work_booking.objects.get(id=id)
    booking.booking_status = 1
    booking.save()
    return redirect('Electrician:my_bookings')

def reject_booking(request, id):
    booking = tbl_work_booking.objects.get(id=id)
    booking.booking_status = 2
    booking.save()
    return redirect('Electrician:my_bookings')

def send_estimate(request, id):
    booking = tbl_work_booking.objects.get(id=id)
    if request.method == 'POST':
        booking.estimate_details = request.POST.get('estimate_details')
        booking.estimate_amount = request.POST.get('estimate_amount')
        booking.booking_status = 3
        booking.save()
        return redirect('Electrician:my_bookings')
    return render(request, 'Electrician/send_estimate.html', {'booking': booking})

def complete_booking(request, id):
    booking = tbl_work_booking.objects.get(id=id)
    booking.booking_status = 4
    booking.save()
    return redirect('Electrician:my_bookings')

# Shopping functions for Electrician
def ajaxplace(request):
    place = tbl_place.objects.filter(district=request.GET.get('pid'))
    return render(request, 'Electrician/ajaxplace.html', {'place': place})

def ajaxsellersearch(request):
    district_id = request.GET.get("district")
    place_id = request.GET.get("place")
    if district_id and place_id:
        seller = tbl_seller.objects.filter(place__id=place_id, place__district__id=district_id)
    elif district_id:
        seller = tbl_seller.objects.filter(place__district__id=district_id)
    else:
        seller = tbl_seller.objects.all()
    return render(request, "Electrician/ajaxsellersearch.html", {"seller": seller})

def viewseller(request):
    district = tbl_district.objects.all()
    seller = tbl_seller.objects.all()
    return render(request, 'Electrician/viewseller.html', {'seller': seller, 'district': district})

def ajaxsubcategory(request):
    subcategory = tbl_subcategory.objects.filter(category=request.GET.get('did'))
    return render(request, 'Electrician/ajaxsubcategory.html', {'subcategory': subcategory})

def ajaxsearch(request):
    ar = [1, 2, 3, 4, 5]
    parry = []
    seller_id = request.GET.get("seller_id")
    if not seller_id:
        return render(request, 'Electrician/ajaxsearch.html', {'msg': "No Product Found"})
    if request.GET.get("cid") and request.GET.get("sid"):
        product = tbl_product.objects.filter(subcategory=request.GET.get("sid"), seller=seller_id)
    elif request.GET.get("cid"):
        product = tbl_product.objects.filter(subcategory__category=request.GET.get("cid"), seller=seller_id)
    else:
        product = tbl_product.objects.filter(seller=seller_id)
    for i in product:
        total_stock = tbl_stock.objects.filter(product=i.id).aggregate(total=Sum('stock_count'))['total']
        total_cart = tbl_cart.objects.filter(product=i.id, cart_status__gt=1).aggregate(total=Sum('cart_qty'))['total']
        if total_stock is None: total_stock = 0
        if total_cart is None: total_cart = 0
        i.total_stock = total_stock - total_cart
        tot = 0
        ratecount = tbl_rating.objects.filter(product=i.id).count()
        if ratecount > 0:
            for j in tbl_rating.objects.filter(product=i.id):
                tot += j.rating_data
            parry.append(tot // ratecount)
        else:
            parry.append(0)
    datas = zip(product, parry)
    return render(request, 'Electrician/ajaxsearch.html', {'product': datas, 'ar': ar})

def viewproduct(request,did):
    ar=[1,2,3,4,5]
    parry=[]
    avg=0
    category=tbl_category.objects.all()
    subcategory=tbl_subcategory.objects.all()
    district=tbl_district.objects.all()
    product = tbl_product.objects.filter(seller_id=did)
    for i in product:
        total_stock = tbl_stock.objects.filter(product=i.id).aggregate(total=Sum('stock_count'))['total']
        total_cart = tbl_cart.objects.filter(product=i.id, cart_status__gt=1).aggregate(total=Sum('cart_qty'))['total']
        if total_stock is None: total_stock = 0
        if total_cart is None: total_cart = 0
        i.total_stock = total_stock - total_cart
        tot=0
        ratecount=tbl_rating.objects.filter(product=i.id).count()
        if ratecount>0:
            ratedata=tbl_rating.objects.filter(product=i.id)
            for j in ratedata: tot=tot+j.rating_data
            avg=tot//ratecount
            parry.append(avg)
        else:
            parry.append(0)
    datas=zip(product,parry)
    return render(request,'Electrician/viewproduct.html',{'product':datas,"ar":ar,'category':category,'subcategory':subcategory,'district':district,"seller_id":did})

def Addcart(request, pid):
    productdata = tbl_product.objects.get(id=pid)
    electrician_data = tbl_electrician.objects.get(id=request.session["did"])
    bookingcount = tbl_booking.objects.filter(electrician=electrician_data, booking_status=0).count()
    if bookingcount > 0:
        bookingdata = tbl_booking.objects.get(electrician=electrician_data, booking_status=0)
        if tbl_cart.objects.filter(booking=bookingdata, product=productdata).exists():
            pass
        else:
            tbl_cart.objects.create(booking=bookingdata, product=productdata, electrician=electrician_data)
    else:
        bookingdata = tbl_booking.objects.create(electrician=electrician_data)
        tbl_cart.objects.create(booking=bookingdata, product=productdata, electrician=electrician_data)
    return redirect("Electrician:Mycart")

def Mycart(request):
    if request.method=="POST":
        bookingdata=tbl_booking.objects.get(id=request.session["ebookingid"])
        bookingdata.booking_amount=request.POST.get("carttotalamt")
        bookingdata.booking_status=1
        bookingdata.save()
        cart = tbl_cart.objects.filter(booking=bookingdata)
        for i in cart:
            i.cart_status = 1
            i.save()
        return redirect("Electrician:productpayment")
    else:
        bookcount = tbl_booking.objects.filter(electrician=request.session["did"],booking_status=0).count()
        if bookcount > 0:
            book = tbl_booking.objects.get(electrician=request.session["did"],booking_status=0)
            request.session["ebookingid"] = book.id
            cart = tbl_cart.objects.filter(booking=book)
            for i in cart:
                total_stock = tbl_stock.objects.filter(product=i.product.id).aggregate(total=Sum('stock_count'))['total']
                total_cart = tbl_cart.objects.filter(product=i.product.id, cart_status=1).aggregate(total=Sum('cart_qty'))['total']
                if total_stock is None: total_stock = 0
                if total_cart is None: total_cart = 0
                total =  total_stock - total_cart
                i.total_stock = total
            return render(request,"Electrician/MyCart.html",{'cartdata':cart})
        else:
            return render(request,"Electrician/MyCart.html")

def DelCart(request,did):
   tbl_cart.objects.get(id=did).delete()
   return redirect("Electrician:Mycart")

def CartQty(request):
   qty=request.GET.get('QTY')
   cartid=request.GET.get('ALT')
   cartdata=tbl_cart.objects.get(id=cartid)
   cartdata.cart_qty=qty
   cartdata.save()
   return redirect("Electrician:Mycart")   

def productpayment(request):
    bookingdata = tbl_booking.objects.get(id=request.session["ebookingid"])
    amt = bookingdata.booking_amount
    cartdata=tbl_cart.objects.filter(booking=request.session['ebookingid'])
    if request.method == "POST":
        bookingdata.booking_status = 2
        bookingdata.save()
        for i in cartdata:
            i.cart_status=2
            i.save()
        return redirect("Electrician:loader")
    else:
        return render(request,"Electrician/Payment.html",{"total":amt})

def loader(request):
    return render(request,"Electrician/Loader.html")
def paymentsuc(request):
    return render(request,"Electrician/Payment_suc.html")

def mybooking(request):
    bookingdata = tbl_booking.objects.filter(electrician=request.session["did"], booking_status__gte=2).order_by('-booking_date')
    return render(request, 'Electrician/MyBooking.html', {'bookingdata': bookingdata})
    
def viewcartproduct(request, id):
    cart = tbl_cart.objects.filter(booking=id)
    return render(request, 'Electrician/Viewcartproducts.html', {'cart': cart})

def work_gallery(request):
    electrician = tbl_electrician.objects.get(id=request.session["did"])
    gallery = tbl_electrician_gallery.objects.filter(electrician=electrician).order_by('-uploaded_at')
    if request.method == "POST":
        photos = request.FILES.getlist('gallery_photo')
        caption = request.POST.get('caption', '')
        for photo in photos:
            if photo:
                tbl_electrician_gallery.objects.create(
                    electrician=electrician,
                    gallery_photo=photo,
                    caption=caption
                )
        return redirect('Electrician:work_gallery')
    
    # Group gallery by caption
    grouped_gallery = {}
    for item in gallery:
        key = item.caption or 'No Caption'
        if key not in grouped_gallery:
            grouped_gallery[key] = []
        grouped_gallery[key].append({
            'id': item.id,
            'gallery_photo': item.gallery_photo.url,
            'uploaded_at': item.uploaded_at,
            'delete_url': f'/electrician/delete_photo/{item.id}/'
        })
    
    return render(request, 'Electrician/work_gallery.html', {'grouped_gallery': grouped_gallery})

def delete_photo(request, photo_id):
    if request.method == 'POST':
        try:
            photo = tbl_electrician_gallery.objects.get(id=photo_id, electrician=request.session["did"])
            photo.delete()
        except tbl_electrician_gallery.DoesNotExist:
            pass
    return redirect('Electrician:work_gallery')

def delete_work(request):
    if request.method == 'POST':
        caption = request.POST.get('caption')
        if caption:
            tbl_electrician_gallery.objects.filter(electrician=request.session["did"], caption=caption).delete()
    return redirect('Electrician:work_gallery')

def view_complaints(request):
    electrician = tbl_electrician.objects.get(id=request.session["did"])
    complaints = tbl_complaint.objects.filter(electrician=electrician, complaint_type=2).order_by('-complaint_date')
    return render(request, 'Electrician/view_complaints.html', {'complaints': complaints})

def reply_complaint(request, complaint_id):
    complaint = tbl_complaint.objects.get(id=complaint_id, electrician=request.session.get("did"))
    if request.method == 'POST':
        reply = request.POST.get('reply')
        complaint.complaint_reply = reply
        complaint.complaint_replydate = __import__('datetime').datetime.now().date()
        complaint.complaint_status = 1
        complaint.save()
        return redirect('Electrician:view_complaints')
    return render(request, 'Electrician/reply_complaint.html', {'complaint': complaint})