from django.shortcuts import render,redirect
from Administrator.models import *
from Guest.models import *
from User.models import *
from datetime import date
from django.conf import settings
from django.core.mail import send_mail
import calendar
import json



# Create your views here.
def logout(request):
    del request.session['aid']
    return redirect('Guest:login')

def adminregistration(request):
    admin=tbl_admin.objects.all()
    if request.method=='POST':
        tbl_admin.objects.create(admin_name=request.POST.get('txt_name'),admin_contact=request.POST.get('txt_contact'),
        admin_email=request.POST.get('txt_email'),admin_password=request.POST.get('txt_password'))
        return redirect('Admin:adminregistration')
        
    else:
         return render(request,'Administrator/AdminRegistration.html',{'admin':admin})


def deleteadmin(request,did):
    tbl_admin.objects.get(id=did).delete()
    return redirect('Admin:adminregistration')

def editadmin(request,did):
    admi=tbl_admin.objects.get(id=did)
    if request.method=="POST":
        admi.admin_name=request.POST.get('txt_name')
        admi.admin_contact=request.POST.get('txt_contact')
        admi.admin_email=request.POST.get('txt_email')
        admi.admin_password=request.POST.get('txt_password')
        admi.save()
        return redirect('Admin:adminregistration')
    else:
        return render(request,'Administrator/AdminRegistration.html',{'editadmin':admi})




def district(request):
    district=tbl_district.objects.all()
    if request.method=='POST':
        tbl_district.objects.create(district_name=request.POST.get('txt_disname'),)
        return redirect('Admin:district')
        
    else:
         return render(request,'Administrator/District.html',{'district':district})


def deletedistrict(request,did):
    tbl_district.objects.get(id=did).delete()
    return redirect('Admin:district')

def editdistrict(request,did):
    dist=tbl_district.objects.get(id=did)
    if request.method=="POST":
        dist.district_name=request.POST.get('txt_disname')
        dist.save()
        return redirect('Admin:district')
    else:
        return render(request,'Administrator/District.html',{'editdist':dist})



def category(request):
    category=tbl_category.objects.all()
    if request.method=='POST':
        tbl_category.objects.create(category_name=request.POST.get('txt_cname'),)
        return redirect('Admin:category')
        
    else:
         return render(request,'Administrator/Category.html',{'category':category})


def deletecategory(request,did):
    tbl_category.objects.get(id=did).delete()
    return redirect('Admin:category')


def editcategory(request,did):
    cat=tbl_category.objects.get(id=did)
    if request.method=="POST":
        cat.category_name=request.POST.get('txt_cname')
        cat.save()
        return redirect('Admin:category')
    else:
        return render(request,'Administrator/Category.html',{'editcat':cat})

def workcategory(request):
    category=tbl_work_category.objects.all()
    if request.method=='POST':
        tbl_work_category.objects.create(work_category_name=request.POST.get('txt_cname'),)
        return redirect('Admin:workcategory')
    else:
         return render(request,'Administrator/WorkCategory.html',{'category':category})

def deleteworkcategory(request,did):
    tbl_work_category.objects.get(id=did).delete()
    return redirect('Admin:workcategory')

def editworkcategory(request,did):
    cat=tbl_work_category.objects.get(id=did)
    if request.method=="POST":
        cat.work_category_name=request.POST.get('txt_cname')
        cat.save()
        return redirect('Admin:workcategory')
    else:
        return render(request,'Administrator/WorkCategory.html',{'editcat':cat})





def place(request):
        District=tbl_district.objects.all()
        placedata=tbl_place.objects.all()
        if request.method=='POST':
            place_name=request.POST.get("pname")
            place_pincode=request.POST.get("pincode")
            district_id=tbl_district.objects.get(id=request.POST.get("district"))
            tbl_place.objects.create(place_name=place_name,district=district_id,place_pincode=place_pincode)
            return redirect('Admin:place')
        else:
            return render(request,'Administrator/Place.html',{'District':District,'placedata':placedata})

def deleteplace(request,did):
    tbl_place.objects.get(id=did).delete()
    return redirect('Admin:place')

def editplace(request,did):
    District=tbl_district.objects.all()
    pla=tbl_place.objects.get(id=did)
    if request.method=="POST":
        pla.place_name=request.POST.get('pname')
        pla.place_pincode=request.POST.get('pincode')
        pla.district=tbl_district.objects.get(id=request.POST.get("district"))
        pla.save()
        return redirect('Admin:place')
    else:
        return render(request,'Administrator/Place.html',{'District':District,'editpla':pla})


def localplace(request):
    district=tbl_district.objects.all()
    localplacedata=tbl_local_place.objects.all()
    if request.method=='POST':
        local_place_name=request.POST.get("pname")
        place_id=tbl_place.objects.get(id=request.POST.get("place"))
        tbl_local_place.objects.create(local_place_name=local_place_name,place=place_id)
        return redirect('Admin:localplace')
    else:
        return render(request,'Administrator/LocalPlace.html',{'district':district,'localplacedata':localplacedata})

def deletelocalplace(request,did):
    tbl_local_place.objects.get(id=did).delete()
    return redirect('Admin:localplace')

def editlocalplace(request,did):
    place=tbl_place.objects.all()
    pla=tbl_local_place.objects.get(id=did)
    if request.method=="POST":
        pla.local_place_name=request.POST.get('pname')
        pla.place=tbl_place.objects.get(id=request.POST.get("place"))
        pla.save()
        return redirect('Admin:localplace')
    else:
        return render(request,'Administrator/LocalPlace.html',{'place':place,'editpla':pla})




def subcategory(request):
        category=tbl_category.objects.all()
        subcategorydata=tbl_subcategory.objects.all()
        if request.method=='POST':
            subcategory_name=request.POST.get("scname")
            category_id=tbl_category.objects.get(id=request.POST.get("category"))
            tbl_subcategory.objects.create(subcategory_name=subcategory_name,category=category_id,)
            return redirect('Admin:subcategory')
        else:
            return render(request,'Administrator/Subcategory.html',{'category':category,'subcategorydata':subcategorydata})

def deletesubcategory(request,did):
    tbl_subcategory.objects.get(id=did).delete()
    return redirect('Admin:subcategory')

def editsubcategory(request,did):
    category=tbl_category.objects.all()
    sub=tbl_subcategory.objects.get(id=did)
    if request.method=="POST":
        sub.subcategory_name=request.POST.get('scname')
        sub.category=tbl_category.objects.get(id=request.POST.get("category"))
        sub.save()
        return redirect('Admin:subcategory')
    else:
        return render(request,'Administrator/Subcategory.html',{'category':category,'editsub':sub})
        



        
def homepage(request):
    user_count = tbl_user.objects.count()
    seller_count = tbl_seller.objects.count()
    electrician_count = tbl_electrician.objects.count()
    
    today = date.today()
    labels = []
    data_list = []
    
    for i in range(5, -1, -1):
        month = today.month - i
        year = today.year
        if month <= 0:
            month += 12
            year -= 1
        count = tbl_work_booking.objects.filter(booking_date__year=year, booking_date__month=month).count()
        labels.append(calendar.month_abbr[month])
        data_list.append(count)

    return render(request,'Administrator/Home.html', {
        'user_count': user_count, 
        'seller_count': seller_count, 
        'electrician_count': electrician_count,
        'growth_labels': json.dumps(labels),
        'growth_data': json.dumps(data_list)
    })




    
def sellerverification(request):
    seller=tbl_seller.objects.filter(seller_status=0)
    return render(request,'Administrator/Sellerverification.html',{'seller':seller})

def electricianverification(request):
    electricians = tbl_electrician.objects.filter(electrician_status=0)
    return render(request,'Administrator/Electricianverification.html',{'electricians': electricians})

def acceptseller(request,did):
    seller=tbl_seller.objects.get(id=did)
    seller.seller_status=1
    seller.save()
    subject = "Seller  Verification Successful"
    body = (f"Respected {seller.seller_name},\n\n"
            f"Your account '{seller.seller_name}' has been successfully verified.\n\n"
            f"Registered Details:\n"
           
            f"Address: {seller.seller_address}\n"
            f"Contact: {seller.seller_contact}\n\n"
            "You can now start using our platform.\n\n"
            "Best Regards,\n Team")
    
    send_mail(
        subject,
        body,
        settings.EMAIL_HOST_USER,
        [seller.seller_email],
        fail_silently=False,
    )
    return redirect('Admin:viewseller')


def rejectseller(request,did):
    seller=tbl_seller.objects.get(id=did)
    seller.seller_status=2
    seller.save()
    subject = "Seller Verification Failed"
    body = (f"Respected {seller.seller_name},\n\n"
            f"Sorry,Your account '{seller.seller_name}' has been rejected.\n\n"
            "Best Regards,\n Team")
    
    send_mail(
        subject,
        body,
        settings.EMAIL_HOST_USER,
        [seller.seller_email],
        fail_silently=False,
    )
    return redirect('Admin:viewseller')


def viewseller(request):
    aseller=tbl_seller.objects.filter(seller_status=1)
    rseller=tbl_seller.objects.filter(seller_status=2)
    if request.method=="POST":
        return redirect('Admin:viewseller')
    else:
         return render(request,'Administrator/viewseller.html',{'aseller':aseller,'rseller':rseller})


def acceptelectrician(request,did):
    electrician=tbl_electrician.objects.get(id=did)
    electrician.electrician_status=1
    electrician.save()
    subject = "Electrician Verification Successful"
    body = (f"Respected {electrician.electrician_name},\n\n"
            f"Your account '{electrician.electrician_name}' has been successfully verified.\n\n"
            f"Registered Details:\n"
           
            f"Address: {electrician.electrician_address}\n"
            f"Contact: {electrician.electrician_contact}\n\n"
            "You can now start using our platform.\n\n"
            "Best Regards,\n Team")
    
    send_mail(
        subject,
        body,
        settings.EMAIL_HOST_USER,
        [electrician.electrician_email],
        fail_silently=False,
    )
    return redirect('Admin:viewelectrician')


def rejectelectrician(request,did):
    rda=tbl_electrician.objects.get(id=did)
    rda.electrician_status=2
    rda.save()
    return redirect('Admin:viewelectrician')

def viewelectrician(request):
    aelectricians = tbl_electrician.objects.filter(electrician_status=1)
    relectricians = tbl_electrician.objects.filter(electrician_status=2)
    if request.method=="POST":
        return redirect('Admin:viewelectrician')
    else:
         return render(request,'Administrator/viewelectrician.html',{'aelectricians':aelectricians,'relectricians':relectricians})

def viewuserfeedback(request):
    user=tbl_user.objects.all()
    feedback=tbl_feedback.objects.filter(user__in=user)
    return render(request,'Administrator/viewfeedback.html',{'feedback':feedback})

def viewsellerfeedback(request):
    seller=tbl_seller.objects.all()
    feedback=tbl_feedback.objects.filter(seller__in=seller)
    return render(request,'Administrator/viewsellerfeedback.html',{'feedback':feedback})

def bookingreport(request):
    if "aid" not in request.session:
        return redirect('Guest:login')
    if  request.method == "POST":
        cart=tbl_cart.objects.filter(booking__booking_date__gt=request.POST.get("txt_fromdate"),booking__booking_date__lt=request.POST.get("txt_todate"))
        return render(request,'Administrator/BookingReport.html',{'cart':cart})
    else:    
        return render(request,'Administrator/BookingReport.html')


