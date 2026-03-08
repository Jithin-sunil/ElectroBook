from django.shortcuts import render, redirect
from django.http import JsonResponse
from Guest.models import *
from Administrator.models import *
from User.models import *
from Seller.models import *
from django.db.models import Sum, Count, Avg
# Create your views here.

def logout(request):
    del request.session['uid']
    return redirect('Guest:login') 

def userhomepage(request):
    electricians = tbl_electrician.objects.filter(electrician_status=1).select_related('local_place', 'work_category')[:6]
    sellers = tbl_seller.objects.all()[:4]
    products = list(tbl_product.objects.select_related('seller', 'subcategory').all()[:8])
    for p in products:
        tot = tbl_rating.objects.filter(product=p.id).aggregate(s=Sum('rating_data'), c=Count('id'))
        p.avg_rating = (tot['s'] or 0) // max(1, tot['c'] or 1) if (tot['c'] or 0) > 0 else 0
    return render(request, 'User/Homepage.html', {
        'electricians': electricians,
        'sellers': sellers,
        'products': products
    })

def myprofile(request):
    user=tbl_user.objects.get(id=request.session["uid"])
    return render(request,'User/MyProfile.html',{'user':user})

def editprofile(request):
    user=tbl_user.objects.get(id=request.session["uid"])
    if request.method=="POST":
        user.user_name=request.POST.get('txt_name')
        user.user_email=request.POST.get('txt_email')
        user.user_contact=request.POST.get('txt_contact')
        user.user_address=request.POST.get('txt_address')
        user.save()
        return redirect('User:myprofile')
    else:
        return render(request,'User/EditProfile.html',{'user':user})

def changepassword(request):
    user=tbl_user.objects.get(id=request.session["uid"])
    dbpass=user.user_password
    if request.method=="POST":
        oldpassword=request.POST.get('txt_oldpass')
        newpassword=request.POST.get('txt_newpass')
        confirmpassword=request.POST.get('txt_conpass')
        if oldpassword==dbpass:
            if newpassword==confirmpassword:
                user.user_password=newpassword
                user.save()
                return redirect("User:myprofile")
    else:
        return render(request,'User/ChangePassword.html',{'user':user})
        

def complaint(request,id):
    userid=tbl_user.objects.get(id=request.session["uid"])
    complaint=tbl_complaint.objects.filter(user=userid)
    productid=tbl_product.objects.get(id=id)
    if request.method=='POST':
        complaint_title=request.POST.get("txt_subname")
        complaint_content=request.POST.get("txt_complaint")
        tbl_complaint.objects.create(complaint_title=complaint_title,complaint_content=complaint_content,user=userid,product=productid)
        return redirect('User:viewcomplaint')
    else:
        return render(request,'User/Postcomplaint.html')

def viewcomplaint(request):
    userid=tbl_user.objects.get(id=request.session["uid"])
    complaint=tbl_complaint.objects.filter(user=userid)
    return render(request,'User/ViewComplaint.html',{'complaint':complaint})




def viewelectricians(request):
    district = tbl_district.objects.all()
    electricians = tbl_electrician.objects.filter(electrician_status=1)
    for e in electricians:
        r = tbl_electrician_rating.objects.filter(electrician=e).aggregate(avg=Avg('rating_data'), cnt=Count('id'))
        e.avg_rating = int(r['avg'] or 0)
        e.rating_count = r['cnt'] or 0
    return render(request, 'User/searchelectrician.html', {'electricians': electricians, 'district': district})

def electrician_rating(request, mid):
    electrician = tbl_electrician.objects.get(id=mid)
    parray = [1, 2, 3, 4, 5]
    ratings = tbl_electrician_rating.objects.filter(electrician=mid).order_by('-datetime')
    counts = ratings.count()
    avg = 0
    if counts > 0:
        res = sum(r.rating_data for r in ratings)
        avg = res // counts
    return render(request, 'User/electrician_rating.html', {
        'electrician': electrician,
        'mid': mid,
        'data': ratings,
        'ar': parray,
        'avg': avg,
        'count': counts
    })

def ajax_electrician_star(request):
    if 'uid' not in request.session:
        from django.http import JsonResponse
        return JsonResponse({'error': 'Please login to rate.'}, status=403)
    parray = [1, 2, 3, 4, 5]
    # Support both GET (legacy) and POST
    data = request.POST if request.method == 'POST' else request.GET
    rating_data = data.get('rating_data')
    user_review = (data.get('user_review') or '').strip()
    eid = data.get('eid')
    if not eid or not rating_data:
        from django.http import JsonResponse
        return JsonResponse({'error': 'Missing rating or electrician.'}, status=400)
    try:
        rating_val = int(rating_data)
        if rating_val < 1 or rating_val > 5:
            raise ValueError('Invalid rating')
    except (TypeError, ValueError):
        from django.http import JsonResponse
        return JsonResponse({'error': 'Invalid rating value.'}, status=400)
    electrician = tbl_electrician.objects.get(id=eid)
    user = tbl_user.objects.get(id=request.session["uid"])
    tbl_electrician_rating.objects.create(
        user=user,
        electrician=electrician,
        user_review=user_review or 'No comment',
        rating_data=rating_val
    )
    ratings = tbl_electrician_rating.objects.filter(electrician=eid).order_by('-datetime')
    counts = ratings.count()
    avg = sum(r.rating_data for r in ratings) // counts if counts > 0 else 0
    return render(request, 'User/ajax_electrician_rating.html', {
        'data': ratings,
        'ar': parray,
        'avg': avg,
        'count': counts
    })

def ajaxelectriciansearch(request):
    district_id = request.GET.get("district")
    place_id = request.GET.get("place")
    local_place_id = request.GET.get("local_place")

    if district_id and place_id and local_place_id:
        electricians = tbl_electrician.objects.filter(local_place__id=local_place_id, local_place__place__id=place_id, local_place__place__district__id=district_id, electrician_status=1)
    elif district_id and place_id:
        electricians = tbl_electrician.objects.filter(local_place__place__id=place_id, local_place__place__district__id=district_id, electrician_status=1)
    elif district_id:
        electricians = tbl_electrician.objects.filter(local_place__place__district__id=district_id, electrician_status=1)
    else:
        electricians = tbl_electrician.objects.filter(electrician_status=1)

    for e in electricians:
        r = tbl_electrician_rating.objects.filter(electrician=e).aggregate(avg=Avg('rating_data'), cnt=Count('id'))
        e.avg_rating = int(r['avg'] or 0)
        e.rating_count = r['cnt'] or 0
    return render(request, "User/ajaxelectriciansearch.html", {"electricians": electricians})

def bookelectrician(request, did):
    if request.method == "POST":
        work_date = request.POST.get("work_date")
        work_details = request.POST.get("work_details")
        electrician = tbl_electrician.objects.get(id=did)
        user = tbl_user.objects.get(id=request.session["uid"])
        tbl_work_booking.objects.create(user=user, electrician=electrician, work_date=work_date, work_details=work_details)
        return redirect("User:myworkbookings")
    return render(request, 'User/bookelectrician.html')

def myworkbookings(request):
    bookings = tbl_work_booking.objects.filter(user=request.session["uid"]).order_by('-booking_date')
    return render(request, 'User/myworkbookings.html', {'bookings': bookings})

def pay_estimate(request, id):
    booking = tbl_work_booking.objects.get(id=id)
    if request.method == "POST":
        booking.booking_status = 4
        booking.save()
        return redirect("User:myworkbookings")
    return render(request, 'User/pay_estimate.html', {'booking': booking})




def Addcart(request,pid):
    productdata=tbl_product.objects.get(id=pid)
    userdata=tbl_user.objects.get(id=request.session["uid"])
    bookingcount=tbl_booking.objects.filter(user=userdata,booking_status=0).count()
    if bookingcount>0:
        bookingdata=tbl_booking.objects.get(user=userdata,booking_status=0)
        cartcount=tbl_cart.objects.filter(booking=bookingdata,product=productdata).count()
        if cartcount>0:
            msg="Already added"
            return render(request,"User/Homepage.html",{'msg':msg})
        else:
            tbl_cart.objects.create(booking=bookingdata,product=productdata)
            msg="Added To cart"
            return render(request,"User/Homepage.html",{'msg':msg})
    else:
        bookingdata = tbl_booking.objects.create(user=userdata)
        tbl_cart.objects.create(booking=tbl_booking.objects.get(id=bookingdata.id),product=productdata)
        msg="Added To cart"
        return render(request,"User/Homepage.html",{'msg':msg})



def Mycart(request):
    if request.method=="POST":
        bookingdata=tbl_booking.objects.get(id=request.session["bookingid"])
        bookingdata.booking_amount=request.POST.get("carttotalamt")
        bookingdata.booking_status=1
        bookingdata.save()
        cart = tbl_cart.objects.filter(booking=bookingdata)
        for i in cart:
            i.cart_status = 1
            i.save()
        return redirect("User:productpayment")
    else:
        bookcount = tbl_booking.objects.filter(user=request.session["uid"],booking_status=0).count()
        if bookcount > 0:
            book = tbl_booking.objects.get(user=request.session["uid"],booking_status=0)
            request.session["bookingid"] = book.id
            cart = tbl_cart.objects.filter(booking=book)
            for i in cart:
                total_stock = tbl_stock.objects.filter(product=i.product.id).aggregate(total=Sum('stock_count'))['total']
                total_cart = tbl_cart.objects.filter(product=i.product.id, cart_status=1).aggregate(total=Sum('cart_qty'))['total']
                # print(total_stock)
                # print(total_cart)
                if total_stock is None:
                    total_stock = 0
                if total_cart is None:
                    total_cart = 0
                total =  total_stock - total_cart
                i.total_stock = total
            return render(request,"User/MyCart.html",{'cartdata':cart})
        else:
            return render(request,"User/MyCart.html")

        

def DelCart(request,did):
   tbl_cart.objects.get(id=did).delete()
   return redirect("User:Mycart")

def CartQty(request):
   qty=request.GET.get('QTY')
   cartid=request.GET.get('ALT')
   cartdata=tbl_cart.objects.get(id=cartid)
   cartdata.cart_qty=qty
   cartdata.save()
   return redirect("User:Mycart")   

def productpayment(request):
    bookingdata = tbl_booking.objects.get(id=request.session["bookingid"])
    amt = bookingdata.booking_amount
    cartdata=tbl_cart.objects.filter(booking=request.session['bookingid'])
    if request.method == "POST":
        bookingdata.booking_status = 2
        bookingdata.save()
        for i in cartdata:
            i.cart_status=2
            i.save()
        return redirect("User:loader")
    else:
        return render(request,"User/Payment.html",{"total":amt})



def loader(request):
    return render(request,"User/Loader.html")

def paymentsuc(request):
    return render(request,"User/Payment_suc.html")

def feedback(request):
    userid=tbl_user.objects.get(id=request.session["uid"])
    feedback=tbl_feedback.objects.filter(user=userid)
    if request.method=='POST':
        feedback_name=request.POST.get("txt_content")
        tbl_feedback.objects.create(feedback_name=feedback_name,user=userid,)
        return redirect('User:feedback')
    else:
        return render(request,'User/Feedback.html',{'feedback':feedback})


def mybooking(request):
    bookingdata = tbl_booking.objects.filter(user=request.session["uid"], booking_status__gte=1).order_by('-booking_date')
    return render(request, 'User/MyBooking.html', {'bookingdata': bookingdata})
    
def viewcartproduct(request,id): 
    cart=tbl_cart.objects.filter(booking=id)
    return render(request,'User/Viewcartproducts.html',{'cart':cart})

def rating(request,mid):
    parray=[1,2,3,4,5]
    mid=mid
    # wdata=tbl_booking.objects.get(id=mid)
    
    counts=0
    counts=stardata=tbl_rating.objects.filter(product=mid).count()
    if counts>0:
        res=0
        stardata=tbl_rating.objects.filter(product=mid).order_by('-datetime')
        for i in stardata:
            res=res+i.rating_data
        avg=res//counts
        # print(avg)
        return render(request,"User/Rating.html",{'mid':mid,'data':stardata,'ar':parray,'avg':avg,'count':counts})
    else:
         return render(request,"User/Rating.html",{'mid':mid})

def ajaxstar(request):
    parray=[1,2,3,4,5]
    rating_data=request.GET.get('rating_data')
    user_name=request.GET.get('user_name')
    user_review=request.GET.get('user_review')
    pid=request.GET.get('pid')
    # wdata=tbl_booking.objects.get(id=pid)
    tbl_rating.objects.create(user=tbl_user.objects.get(id=request.session["uid"]),user_review=user_review,rating_data=rating_data,product=tbl_product.objects.get(id=pid))
    stardata=tbl_rating.objects.filter(product=pid).order_by('-datetime')
    return render(request,"User/AjaxRating.html",{'data':stardata,'ar':parray})

def starrating(request):
    r_len = 0
    five = four = three = two = one = 0
    # cdata = tbl_booking.objects.get(id=request.GET.get("pdt"))
    rate = tbl_rating.objects.filter(product=request.GET.get("pdt"))
    ratecount = tbl_rating.objects.filter(product=request.GET.get("pdt")).count()
    for i in rate:
        if int(i.rating_data) == 5:
            five = five + 1
        elif int(i.rating_data) == 4:
            four = four + 1
        elif int(i.rating_data) == 3:
            three = three + 1
        elif int(i.rating_data) == 2:
            two = two + 1
        elif int(i.rating_data) == 1:
            one = one + 1
        else:
            five = four = three = two = one = 0
        # print(i.rating_data)
        # r_len = r_len + int(i.rating_data)
    # rlen = r_len // 5
    # print(rlen)
    result = {"five":five,"four":four,"three":three,"two":two,"one":one,"total_review":ratecount}
    return JsonResponse(result)



def ajaxsubcategory(request):
    subcategory=tbl_subcategory.objects.filter(category=request.GET.get('did'))
    return render(request,'User/ajaxsubcategory.html',{'subcategory':subcategory})


def ajaxplace(request):
    place=tbl_place.objects.filter(district=request.GET.get('pid'))
    return render(request,'User/ajaxplace.html',{'place':place})

def ajaxlocalplace(request):
    local_place=tbl_local_place.objects.filter(place=request.GET.get('pid'))
    return render(request,'Guest/ajaxlocalplace.html',{'local_place':local_place})


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
        # print(total_stock)
        # print(total_cart)
        if total_stock is None:
            total_stock = 0
        if total_cart is None:
            total_cart = 0
        total =  total_stock - total_cart
        i.total_stock = total


        tot=0
        ratecount=tbl_rating.objects.filter(product=i.id).count()
        if ratecount>0:
            ratedata=tbl_rating.objects.filter(product=i.id)
            for j in ratedata:
                tot=tot+j.rating_data
                avg=tot//ratecount
                #print(avg)
            parry.append(avg)
        else:
            parry.append(0)
        # print(parry)
    datas=zip(product,parry)
    return render(request,'User/viewproduct.html',{'product':datas,"ar":ar,'category':category,'subcategory':subcategory,'district':district,"seller_id":did})



def ajaxsearch(request):
    
    if (request.GET.get("cid")) and (request.GET.get("sid")):
        ar=[1,2,3,4,5]
        parry=[]
        avg=0
        product=tbl_product.objects.filter(subcategory=request.GET.get("sid"),seller=request.GET.get("seller_id"))

        for i in product:
            total_stock = tbl_stock.objects.filter(product=i.id).aggregate(total=Sum('stock_count'))['total']
            total_cart = tbl_cart.objects.filter(product=i.id, cart_status=1).aggregate(total=Sum('cart_qty'))['total']
            # print(total_stock)
            # print(total_cart)
            if total_stock is None:
                total_stock = 0
            if total_cart is None:
                total_cart = 0
            total =  total_stock - total_cart
            i.total_stock = total


            tot=0
            ratecount=tbl_rating.objects.filter(product=i.id).count()
            if ratecount>0:
                ratedata=tbl_rating.objects.filter(product=i.id)
                for j in ratedata:
                    tot=tot+j.rating_data
                    avg=tot//ratecount
                    #print(avg)
                parry.append(avg)
            else:
                parry.append(0)
            # print(parry)
        datas=zip(product,parry)
        return render(request,'User/ajaxsearch.html',{'product':datas,'ar':ar})
    elif (request.GET.get("cid")):
        ar=[1,2,3,4,5]
        parry=[]
        avg=0
        product=tbl_product.objects.filter(subcategory__category=request.GET.get("cid"),seller=request.GET.get("seller_id"))

        for i in product:
            total_stock = tbl_stock.objects.filter(product=i.id).aggregate(total=Sum('stock_count'))['total']
            total_cart = tbl_cart.objects.filter(product=i.id, cart_status=1).aggregate(total=Sum('cart_qty'))['total']
            # print(total_stock)
            # print(total_cart)
            if total_stock is None:
                total_stock = 0
            if total_cart is None:
                total_cart = 0
            total =  total_stock - total_cart
            i.total_stock = total


            tot=0
            ratecount=tbl_rating.objects.filter(product=i.id).count()
            if ratecount>0:
                ratedata=tbl_rating.objects.filter(product=i.id)
                for j in ratedata:
                    tot=tot+j.rating_data
                    avg=tot//ratecount
                    #print(avg)
                parry.append(avg)
            else:
                parry.append(0)
            # print(parry)
        datas=zip(product,parry)
        return render(request,'User/ajaxsearch.html',{'product':datas,'ar':ar})
    else:
        return render(request,'User/ajaxsearch.html',{'msg':"No Product Found"})




def viewseller(request):
    district = tbl_district.objects.all()
    seller = tbl_seller.objects.all()
    return render(request, 'User/viewseller.html', {'seller': seller, 'district': district})

def ajaxsellersearch(request):
    district_id = request.GET.get("district")
    place_id = request.GET.get("place")

    if district_id and place_id:
        seller = tbl_seller.objects.filter(place__id=place_id, place__district__id=district_id)
    elif district_id:
        seller = tbl_seller.objects.filter(place__district__id=district_id)
    else:
        seller = tbl_seller.objects.all()

    return render(request, "User/ajaxsellersearch.html", {"seller": seller})